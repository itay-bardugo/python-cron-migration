from .mapper import RevisionMapper
from cron_migration.revisions.manager import TaskManager
from cron_migration.app.models.environment import Environment
import json


class RevisionApply:
    def __init__(self, mapper: RevisionMapper, environment: Environment):
        self._mapper = mapper
        self._environment = environment
        self._mapper.review()

    def _save_last_revision(self, revision: TaskManager, tail: str):
        with open(self._environment.path_from_base('.rvsn'), "r+") as f:
            try:
                json_ = json.load(f)
            except json.JSONDecodeError:
                json_ = {}
            json_[tail] = revision.get_revision_id() if revision is not None else ""
            f.seek(0)
            f.truncate()
            json.dump(json_, f)

    def upgrade(self, revision: TaskManager):
        revision.upgrade()
        if not revision.next:
            self._save_last_revision(revision, self._mapper.get_tail_from_head(revision))

    def downgrade(self, revision: TaskManager, tail: str):
        revision.downgrade()
        self._save_last_revision(self._mapper.revisions.get(revision.get_down_revision(), None), tail)

    def get_downgrades_list(self, steps):
        revision_signature = self._mapper.get_latest_revision()
        if self._mapper.total_heads() > 1:
            raise Exception("Please Merge files before downgrading....")
        for _ in range(int(steps), 0, -1):
            if not revision_signature:
                break
            revision = self._mapper.revisions[revision_signature]
            yield revision
            revision_signature = revision.get_down_revision()

    def get_upgrades_list(self):
        return self._mapper.get_waiting_list()

    def get_tail_from_head(self, revision: TaskManager):
        return self._mapper.get_tail_from_head(revision)
