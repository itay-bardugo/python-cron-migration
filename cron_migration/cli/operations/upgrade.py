from cron_migration.revisions.services.upgrade import UpgradeService
from cron_migration.cli.models.command import BaseCommand
from cron_migration.cli.manager import CommandsManager


@CommandsManager.bind("upgrade")
class Upgrade(BaseCommand):
    def __init__(self, upgrade_service: UpgradeService):
        self._upgrade_service = upgrade_service

    def run(self):
        BaseCommand._output.header(f"listing files")
        for revision in self._upgrade_service.get_waiting_list():
            log = BaseCommand._output.printed_task(
                BaseCommand._output.blue,
                f"file: {revision.path}, revision id: {revision.get_revision_id()}",
                BaseCommand._output.green,
                "Done",
                BaseCommand._output.red,
                "Failed!",
                success_indicator=None
            )(lambda: self._upgrade_service.upgrade(revision))
            log()

        return None
