import os
import shutil
from cron_migration.files.models.path import Path
from cron_migration.app import exist_codes


def copy_tree(src: Path, dest: Path):
    try:
        shutil.copytree(src.path, dest.path)
    except Exception as e:
        return exist_codes.COULD_NOT_COPY_FILES


def mkdir(path: Path):
    try:
        os.mkdir(path.path)
    except Exception:
        return False
    return True
