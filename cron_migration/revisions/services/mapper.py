from cron_migration.app.models.environment import Environment
import os
import importlib.util
import json
from typing import Iterator, Set, Dict
from cron_migration.revisions.manager import TaskManager


class RevisionMapper:
    def __init__(self, environment: Environment):
        self._environment = environment
        self.revisions: Dict[str, TaskManager] = {}
        self.latest: Set[str] = set()
        self._last_upgraded_revision = ""
        self._first_revision: TaskManager = None
        self._heads: Dict[str, TaskManager] = {}
        self._tails: Dict[str, TaskManager] = {}

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
                self._tails[revision.get_revision_id()] = revision
            self.latest.add(revision.get_revision_id())

        for revision in self.revisions.values():
            if revision.get_down_revision() is None:
                continue
            prev_revision = self.revisions[revision.get_down_revision()]
            prev_revision.set_next(revision.task)
            if prev_revision.get_revision_id() in self.latest:
                self.latest.discard(prev_revision.get_revision_id())

        for revision_id in self._tails:
            tail = revision_id
            revision = self.revisions[revision_id]
            while revision:
                revision_id = revision.get_revision_id()
                revision = self.revisions[revision.get_revision_id()].next

            self._tails[tail] = self.revisions[revision_id]  # start to end
            self._heads[revision_id] = self.revisions[tail]  # end to start

    def total_heads(self):
        return len(self._heads)

    def get_latest_revision(self):
        for revision_id in self.latest:
            return revision_id
        return None

    @property
    def get_revision_to_upgrade(self):
        with open(self._environment.path_from_base('.rvsn'), "r") as f:
            json_ = {}
            for tail in self._tails:
                try:
                    json_ = json.load(f) if not json_ else json_
                except json.JSONDecodeError:
                    json_ = {}
                try:
                    # todo handle error
                    revision_key = tail
                    if revision_line := json_.get(tail, None):
                        if not self.revisions[revision_line].next:
                            raise Exception()
                        revision_key = self.revisions[revision_line].next.get_revision_id()

                    yield revision_key
                except (FileNotFoundError, Exception):
                    continue

    def get_tail_from_head(self, revision: TaskManager):
        return self._heads[revision.get_revision_id()].get_revision_id()

    def get_head_from_tail(self, revision: TaskManager):
        return self._tails[revision.get_revision_id()].get_revision_id()

    def _get_first_revision(self):
        return self._first_revision

    def get_waiting_list(self):
        for revision_to_update in self.get_revision_to_upgrade:
            revision = self.revisions[revision_to_update]
            while revision:
                yield (self.revisions[revision.get_revision_id()])
                revision = self.revisions[revision.get_revision_id()].next
