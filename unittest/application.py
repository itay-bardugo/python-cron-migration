import unittest
from unittest import TestCase
import subprocess
import sys
import os
import shutil


class ApplicationTest(TestCase):
    def test_init(self):
        proc = subprocess.Popen(["cronmig", "init"])
        self.assertEqual(proc.wait(), 0)

    def test_revision_make(self):
        proc = subprocess.Popen(["cronmig-revision", "make", "test revision"])
        self.assertEqual(proc.wait(), 0)

    def test_revision_upgrade(self):
        proc = subprocess.Popen(["cronmig-revision", "upgrade"])
        self.assertEqual(proc.wait(), 0)

    def test_revision_downgrade(self):
        proc = subprocess.Popen(["cronmig-revision", "downgrade", "3"])
        self.assertEqual(proc.wait(), 0)

    def test_app(self):
        try:
            self.test_init()
            self.test_revision_make()
            self.test_revision_upgrade()
            self.test_revision_downgrade()
        finally:
            shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cronjobs"))


if __name__ == '__main__':
    unittest.main(exit=False)
