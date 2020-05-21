import click
import os
from cron_migration.app.services.init import new_env
from cron_migration.app.models.new_environment import NewEnvironment
from cron_migration.files.models.path import Path


@click.command()
@click.option('-n', '--dir-name', default="cronjobs")
def init(dir_name):
    env = NewEnvironment()
    env.path = Path(os.path.join(os.getcwd(), dir_name))
    env.template = "default"
    exit(new_env.create(env))


if __name__ == '__main__':
    init()
