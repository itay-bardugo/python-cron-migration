import click
import os
from cron_migration.cli import environment
from cron_migration.files.models.path import Path
from cron_migration.cli import OperationsFacade
from cron_migration.revisions.model import Revision
from cron_migration.revisions.services.new_revision import NewRevisionService
from cron_migration.revisions.services.revision_apply import RevisionApply
from cron_migration.revisions.services.mapper import RevisionMapper


@click.group()
def cronmig():
    ...


@cronmig.command()
@click.option('-n', '--dir-name', default="cronjobs")
def init(dir_name):
    """Creates a new envrionment"""
    environment.path = Path(os.path.join(os.getcwd(), dir_name))
    exit(int(OperationsFacade.init(environment)))


@click.group()
def revision():
    ...


@revision.command()
@click.option('-n', '--dir-name', default="cronjobs")
@click.option('-h', '--head', is_flag=True)
@click.argument("message")
def make(message, dir_name, head):
    environment.path = Path(os.path.join(os.getcwd(), dir_name))
    environment.head = head
    revision_service = NewRevisionService(Revision(), RevisionMapper(environment), environment)
    exit(int(OperationsFacade.make_revision(revision_service, message)))


@revision.command()
@click.option('-n', '--dir-name', default="cronjobs")
def upgrade(dir_name):
    environment.path = Path(os.path.join(os.getcwd(), dir_name))
    service = RevisionApply(RevisionMapper(environment), environment)
    exit(int(OperationsFacade.upgrade(service)))


@revision.command()
@click.argument("steps")
@click.option('-n', '--dir-name', default="cronjobs")
def downgrade(steps, dir_name):
    environment.path = Path(os.path.join(os.getcwd(), dir_name))
    service = RevisionApply(RevisionMapper(environment), environment)
    exit(int(OperationsFacade.downgrade(service, steps)))


if __name__ == '__main__':
    ...
    # init()
    # revision()
