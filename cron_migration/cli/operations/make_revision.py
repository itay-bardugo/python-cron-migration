from cron_migration.revisions.services.new_revision import NewRevisionService
from cron_migration.cli.models.command import BaseCommand
from cron_migration.cli.manager import CommandsManager


@CommandsManager.bind("make_revision")
class MakeRevision(BaseCommand):
    def __init__(self, _new_revision_service: NewRevisionService, message):
        self._new_revision_service = _new_revision_service
        self._message = message

    def run(self):
        self._new_revision_service.create_revision(self._message)

        return None
