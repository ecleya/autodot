import os
import shutil
import tempfile
from unittest import TestCase, mock

from collectors import brew_cask


PACKAGES = b'''
a
b
c
'''


class TestProject(TestCase):
    @mock.patch('subprocess.check_output')
    def test_installed_packages(self, mock_check_output):
        mock_check_output.return_value = PACKAGES

        packages = [package for package in brew_cask.packages()]
        self.assertEquals(packages, ['a', 'b', 'c'])
