import subprocess


class Driver:
    def __init__(self):
        self._options = {}


    def _exec(self):
        options = ["{} {}".format(k, v).strip() for k, v in self._options.items()]
        self._options = {}
        process = subprocess.Popen(["crontab"] + options, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = process.wait()
        result = (exit_code, process.stdout, process.stderr)
        return result

    def add_option(self, key, value=""):
        self._options[key] = value

    def all_jobs(self):
        self.add_option("-l")
        return self._exec()

    def user(self, u):
        self.add_option("-u", u)

    def delete(self):
        self.add_option("-r")
        return self._exec()

    def insert(self, filepath):
        self.add_option(filepath)
        self._exec()