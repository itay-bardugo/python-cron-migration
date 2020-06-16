import subprocess


class Driver:
    def __init__(self):
        self._options = {}
        self._const_options = {}

    def _exec(self):
        options = [arg for k, v in self._const_options.items() for arg in ([k]+[v] if v else [k])]
        options += [arg for k, v in self._options.items() for arg in ([k]+[v] if v else [k])]
        self._options = {}
        process = subprocess.Popen(["crontab"] + options, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = process.wait()
        result = (exit_code, process.stdout, process.stderr)
        return result

    def add_option(self, key, value=""):
        self._options[key] = value

    def add_const_option(self, key, value=""):
        self._const_options[key] = value

    def all_jobs(self):
        self.add_option("-l")
        return self._exec()

    def user(self, u):
        self.add_const_option("-u", u)

    def delete(self):
        self.add_option("-r")
        return self._exec()

    def insert(self, filepath):
        self.add_option(filepath)
        self._exec()
