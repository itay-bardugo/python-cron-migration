from cron_migration.app import manager as app_manager
from cron_migration.files.managers import files as files_manager
from cron_migration.files.models.path import Path
from cron_migration.files.managers.path import PathManager
from cron_migration.app.models.new_environment import NewEnvironment
from cron_migration.app import exist_codes


def create(env: NewEnvironment) -> int:
    path_manager = PathManager()
    path_manager.set_path(env.path)
    if path_manager.is_dir():
        return exist_codes.FOLDER_ALREADY_EXISTS

    if isinstance(template := app_manager.get_template(env.template), int):
        return template

    src = Path(template)
    files_manager.copy_tree(src, env.path)

    if not path_manager.has_access():
        if (path_manager.remove_tree()) is not True:
            return exist_codes.COULD_NOT_REMOVE_BASE_FOLDER
        return exist_codes.PATH_NO_ACCESS

    return 0
