from cron_migration.cli.models.command import Command
from typing import Dict, Union, Callable


class CommandsManager:
    __commands: Dict[str, Union[Callable[..., Command], Command]] = {}

    def __init__(self):
        self._request = ""

    def __getattr__(self, item):
        self._request = item

        def wrapper(*args, **kwargs):
            return self._get_app(*args, **kwargs).run()

        return wrapper

    def _get_app(self, *args, **kwargs):
        target = self._get_command()
        if self._instance_exists():
            return target
        return target(*args, **kwargs)

    def _get_command(self):
        return CommandsManager.__commands[self._request]

    def _instance_exists(self):
        return True if isinstance(self._get_command(), Command) else False

    @staticmethod
    def bind(alias: str):
        assert alias not in CommandsManager.__commands, "alias '{}' already exists".format(alias)

        def wraper(cls: Callable[..., Command]):
            def callback(*args, **kwargs):
                return cls(*args, **kwargs)

            CommandsManager.__commands[alias] = callback

        return wraper
