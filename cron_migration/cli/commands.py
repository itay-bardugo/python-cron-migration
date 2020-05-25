import click
import os
from cron_migration.app.models.new_environment import NewEnvironment
from cron_migration.files.models.path import Path
from cron_migration.cli import OperationsFacade


@click.command()
@click.option('-n', '--dir-name', default="cronjobs")
def init(dir_name):
    exit(OperationsFacade.init(NewEnvironment(path=Path(os.path.join(os.getcwd(), dir_name)))))


if __name__ == '__main__':
    init()
