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

    def stream_revisions(self) -> Iterator[TaskManager]:
        revision_path = self._environment.get_revisions_path()
        for module_ in os.listdir(revision_path.path):
            if "__pycache__" in module_:
                continue

            spec = importlib.util.spec_from_file_location(module_, f"{revision_path.join(module_)}")
            revision = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(revision)
            yield TaskManager(revision.Revision)

    def review(self):
        for revision in self.stream_revisions():
            if revision.get_revision_id() in self.revisions:
                # handle error
                continue

            self.revisions[revision.get_revision_id()] = revision
            self.latest.add(revision.get_revision_id())

        for revision in self.revisions.values():
            if revision.get_down_revision() is None:
                continue
            prev_revision = self.revisions[revision.get_down_revision()]
            revision.set_next(prev_revision.task)
            if prev_revision.get_revision_id() in self.latest:
                self.latest.discard(prev_revision.get_revision_id())

    def get_latest_revision(self):
        for revision_id in self.latest:
            return revision_id
        return None
