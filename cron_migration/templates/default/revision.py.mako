from cron_migration.revisions.task import Task


class Revision(Task):
    def upgrade(self):
        pass

    def downgrade(self):
        pass

    @classmethod
    def get_revision_id(cls) -> str:
        return "${revision}"

    @classmethod
    def get_prev_revision_id(cls) -> str:
        % if prev_revision is None:
        return ""
        % else:
        return "${prev_revision}"
        % endif

