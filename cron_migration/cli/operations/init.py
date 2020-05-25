from cron_migration.app import manager as app_manager
from cron_migration.files.managers import files as files_manager
from cron_migration.files.models.path import Path
from cron_migration.files.managers.path import PathManager
from cron_migration.app.models.new_environment import NewEnvironment
from cron_migration.app import exist_codes
from cron_migration.cli.models.command import BaseCommand
from cron_migration.cli.manager import CommandsManager


@CommandsManager.bind("init")
class Init(BaseCommand):
    def __init__(self, env: NewEnvironment):
        self._env = env
        self._path_manager = PathManager()
        self._path_manager.set_path(self._env.path)
        self._template = None

    @BaseCommand._output.printed_task(
        BaseCommand._output.blue,
        "Checking if path is already exist",
        BaseCommand._output.header,
        "Done.",
        BaseCommand._output.red,
        "Path is already exists",
        None
    )
    def _path_exists(self):
        if self._path_manager.is_dir():
            return exist_codes.FOLDER_ALREADY_EXISTS
        return None

    @BaseCommand._output.printed_task(
        BaseCommand._output.blue,
        "looking for a template",
        BaseCommand._output.header,
        "Done.",
        BaseCommand._output.red,
        "Template is not exists",
        str()
    )
    def _get_template(self):
        return app_manager.get_template(self._env.template)

    @BaseCommand._output.printed_task(
        BaseCommand._output.blue,
        "Copying files...",
        BaseCommand._output.header,
        "Done.",
        success_indicator=None
    )
    def _copy_files(self):
        if isinstance(err := files_manager.copy_tree(Path(self._template), self._env.path), int):
            return err
        return None

    @BaseCommand._output.printed_task(
        BaseCommand._output.blue,
        "can not access, trying to remove",
        BaseCommand._output.header,
        "removed successfully",
        BaseCommand._output.red,
        "Could not remove tree, please remove it manually",
        None
    )
    def _remove_files(self):
        if (self._path_manager.remove_tree()) is not True:
            return exist_codes.COULD_NOT_REMOVE_BASE_FOLDER
        return None

    @BaseCommand._output.printed_task(
        BaseCommand._output.blue,
        "Validate environment access",
        on_fail_color=BaseCommand._output.red,
        on_fail_msg="Could not remove tree, please remove it manually",
        success_indicator=True
    )
    def _validate_access(self):
        if not self._path_manager.has_access():
            if error := self._remove_files():
                return error
            return exist_codes.PATH_NO_ACCESS
        return True

    @BaseCommand._output.printed_task(
        BaseCommand._output.blue,
        "Preparing environment.....",
        BaseCommand._output.green,
        "Done.",
        BaseCommand._output.red,
        "Failed!",
        success_indicator=None
    )
    def run(self):
        if error := self._path_exists():
            return error

        if not isinstance(template := self._get_template(), str):
            return template
        self._template = template
        self._copy_files()
        if not isinstance(has_access := self._validate_access(), bool):
            return has_access

        return None
