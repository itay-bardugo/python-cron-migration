from cron_migration.files.models.path import Path
import os


class Environment:
    def __init__(self, path: Path = None, template: str = "default", head: bool = False):
        self._path = path
        self.template = template
        self.head = head

    def get_real_path(self):
        return self.path.path

    def save_last_head(self, signature):
        try:
            with open(self.path_from_base('.rvsn'), "w") as f:
                f.write(signature)
        except:
            return False
        return True

    def get_last_head(self):
        last = None
        try:
            with open(self.path_from_base('.rvsn'), "r") as f:
                last = f.readline() or last
        except:
            ...
        finally:
            return last

    def get_script_path(self) -> Path:
        return Path(
            path=os.path.join(
                self.get_real_path() +
                os.path.sep +
                "revision.py.mako"
            )
        )

    def path_from_base(self, *args):
        return self._path.join(*args)

    def get_revisions_path(self, filename=None) -> Path:
        return Path(
            path=os.path.join(
                self.get_real_path() +
                os.path.sep +
                "revisions" +
                (os.path.sep + filename if filename else "")

            )
        )

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, p):
        self._path = p
