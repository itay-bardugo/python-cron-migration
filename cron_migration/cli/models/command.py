from abc import ABCMeta, abstractmethod
from cron_migration.cli.output import Output
from .commandError import CommandError


class Command(metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        ...


class BaseCommand(Command):
    _output = Output()

    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def fail(error_code=None):
        raise CommandError(error_code=error_code)
