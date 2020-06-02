import click
import os
from cron_migration.cli import environment
from cron_migration.files.models.path import Path
from cron_migration.cli import OperationsFacade
from cron_migration.revisions.model import Revision
from cron_migration.revisions.services.new_revision import NewRevisionService
from cron_migration.revisions.services.mapper import RevisionMapper


@click.command()
@click.option('-n', '--dir-name', default="cronjobs")
def init(dir_name):
    """Creates a new envrionment"""
    environment.path = Path(os.path.join(os.getcwd(), dir_name))
    OperationsFacade.init(environment)


@click.group()
def revision():
    ...


@revision.command()
@click.option('-n', '--dir-name', default="cronjobs")
@click.argument("message")
def make(message, dir_name):
    environment.path = Path(os.path.join(os.getcwd(), dir_name))
    revision_service = NewRevisionService(Revision(), RevisionMapper(environment), environment)
    OperationsFacade.make_revision(revision_service, message)


if __name__ == '__main__':
    #init()
    revision()
