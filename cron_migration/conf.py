import os
from cron_migration.files.models.path import Path

root = Path(os.path.dirname(os.path.abspath(__file__)))
templates = Path(os.path.join(root.path, *["templates"]))
