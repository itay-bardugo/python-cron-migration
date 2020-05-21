from cron_migration.revisions.task import Task


class Revision(Task):
    def upgrade(self):
        pass

    def downgrade(self):
        pass

    @classmethod
    def get_revision_id(cls) -> str:
        return ""

    @classmethod
    def get_prev_revision_id(cls) -> str:
        pass

