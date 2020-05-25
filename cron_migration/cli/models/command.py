from abc import ABCMeta, abstractmethod
from cron_migration.cli.output import Output


class Command(metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        ...


class BaseCommand(Command):
    _output = Output()

    @abstractmethod
    def run(self):
        pass
