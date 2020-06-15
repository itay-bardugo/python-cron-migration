from .mapper import RevisionMapper
from cron_migration.revisions.manager import TaskManager
from cron_migration.app.models.environment import Environment


class RevisionApply:
    def __init__(self, mapper: RevisionMapper, environment: Environment):
        self._mapper = mapper
        self._environment = environment
        self._mapper.review()

    def _save_last_revision(self, revision: TaskManager):
        with open(self._environment.path_from_base('.rvsn'), "w") as f:
            f.write(revision.get_revision_id() if revision is not None else "")

    def upgrade(self, revision: TaskManager):
        revision.upgrade()
        if not revision.next:
            self._save_last_revision(revision)

    def downgrade(self, revision: TaskManager):
        revision.downgrade()
        self._save_last_revision(self._mapper.revisions.get(revision.get_down_revision(), None))

    def get_downgrades_list(self, steps):
        revision_signature = self._mapper.get_latest_revision()
        for _ in range(int(steps), 0, -1):
            if not revision_signature:
                break
            revision = self._mapper.revisions[revision_signature]
            yield revision
            revision_signature = revision.get_down_revision()

    def get_upgrades_list(self):
        return self._mapper.get_waiting_list()
