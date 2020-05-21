from cron_migration.conf import templates
from cron_migration.files.managers.path import PathManager
from cron_migration.files.models.path import Path
from cron_migration.app import exist_codes
import os


def get_templates_path():
    return templates.path


def get_template(template):
    path = Path(os.path.join(get_templates_path(), template))
    path_manager = PathManager()
    path_manager.set_path(path)
    if not path_manager.is_dir():
        return exist_codes.INVALID_TEMPLATE
    return path.path
