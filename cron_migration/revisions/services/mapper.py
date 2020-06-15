from cron_migration.app.models.environment import Environment
import os
import importlib.util
from typing import Iterator, Set, Dict
from cron_migration.revisions.manager import TaskManager


class RevisionMapper:
    def __init__(self, environment: Environment):
        self._environment = environment
        self.revisions: Dict[str, TaskManager] = {}
        self.latest: Set[str] = set()
        self._last_upgraded_revision = ""
        self._first_revision: TaskManager = None

    def stream_revisions(self) -> Iterator[TaskManager]:
        revision_path = self._environment.get_revisions_path()
        for module_ in os.listdir(revision_path.path):
            if "__pycache__" in module_:
                continue

            module_path = revision_path.join(module_)
            spec = importlib.util.spec_from_file_location(module_, f"{module_path}")
            revision = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(revision)
            yield TaskManager(revision.Revision, module_path)

    def review(self):
        for revision in self.stream_revisions():
            if revision.get_revision_id() in self.revisions:
                # todo: handle error: duplicate
                continue
            self.revisions[revision.get_revision_id()] = revision
            if revision.get_down_revision() is None:
                self._first_revision = revision
            self.latest.add(revision.get_revision_id())

        for revision in self.revisions.values():
            if revision.get_down_revision() is None:
                continue
            prev_revision = self.revisions[revision.get_down_revision()]
            prev_revision.set_next(revision.task)
            if prev_revision.get_revision_id() in self.latest:
                self.latest.discard(prev_revision.get_revision_id())

    def get_latest_revision(self):
        for revision_id in self.latest:
            return revision_id
        return None

    @property
    def get_revision_to_upgrade(self):
        if self._last_upgraded_revision is str():
            try:
                with open(self._environment.path_from_base('.rvsn'), "r") as f:
                    # todo handle error
                    revision_key = self._get_first_revision().get_revision_id()
                    if revision_line := f.readline():
                        if not self.revisions[revision_line].next:
                            raise Exception("Nothing to upgrade")
                        revision_key = self.revisions[revision_line].next.get_revision_id()

                    self._last_upgraded_revision = revision_key
            except FileNotFoundError:
                self._last_upgraded_revision = None

        return self._last_upgraded_revision

    def _get_first_revision(self):
        return self._first_revision

    def get_waiting_list(self):
        revision = self.revisions[self.get_revision_to_upgrade]
        while revision:
            yield (self.revisions[revision.get_revision_id()])
            revision = self.revisions[revision.get_revision_id()].next
