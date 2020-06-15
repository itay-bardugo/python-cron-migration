from cron_migration.cli.models.command import BaseCommand
from cron_migration.cli.manager import CommandsManager
from cron_migration.revisions.services.revision_apply import RevisionApply


@CommandsManager.bind("downgrade")
class Downgrade(BaseCommand):
    def __init__(self, service: RevisionApply, steps: int):
        self._service = service
        self._steps = steps

    def run(self):
        for revision in self._service.get_downgrades_list(self._steps):
            log = BaseCommand._output.printed_task(
                BaseCommand._output.blue,
                f"downgrading file: {revision.path}, revision id: {revision.get_revision_id()}",
                BaseCommand._output.green,
                "Done",
                BaseCommand._output.red,
                "Failed!",
                success_indicator=None
            )(lambda: self._service.downgrade(revision))
            log()

        return 0
