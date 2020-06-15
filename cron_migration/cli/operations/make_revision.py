from cron_migration.revisions.services.new_revision import NewRevisionService
from cron_migration.cli.models.command import BaseCommand
from cron_migration.cli.manager import CommandsManager


@CommandsManager.bind("make_revision")
class MakeRevision(BaseCommand):
    def __init__(self, _new_revision_service: NewRevisionService, message):
        self._new_revision_service = _new_revision_service
        self._message = message

    def run(self):
        filename = self._new_revision_service.make_revision_file(self._message)
        log = BaseCommand._output.printed_task(
            BaseCommand._output.blue,
            "generating revision file...",
            BaseCommand._output.green,
            filename,
            BaseCommand._output.red,
            "Failed!",
            success_indicator=str
        )(lambda: filename)
        log()

        return 0
