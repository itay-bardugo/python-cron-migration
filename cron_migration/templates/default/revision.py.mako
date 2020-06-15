from cron_migration.revisions.task import Task
from cron_migration.suits.crontab.crontab import Crontab
from cron_migration.suits.crontab.scheduler import Scheduler

"""
Date: ${date}
message: ${message}
"""


class Revision(Task):

    def __init__(self) -> None:
        super().__init__()
        self.command = ""  # your crontab command here
        self.timing = {
            'minute': "*",
            'hour': "*",
            'month_day': "*",
            'month': "*",
            'week_day': "*"
        }

    def upgrade(self):
        crontab = Crontab(user=None)
        job = crontab.new_job(command=self.command, **self.timing)
        # scheduler = Scheduler()
        # scheduler.at_midnight()
        # job.scheduler = scheduler
        crontab.insert(job)

    def downgrade(self):
        crontab = Crontab(user=None)
        job = crontab.new_job(command=self.command, **self.timing)
        # scheduler = Scheduler()
        # scheduler.at_midnight()
        # job.scheduler = scheduler
        crontab.remove(job)

    @classmethod
    def get_revision_id(cls) -> str:
        return "${revision}"

    @classmethod
    def get_prev_revision_id(cls) -> str:
        % if prev_revision is None:
        return None
        % else:
        return "${prev_revision}"
        % endif

