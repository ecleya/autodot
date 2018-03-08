import os
import shutil
import tempfile
from unittest import TestCase, mock

from collectors import app_store


APPS = b'''
497799835 Xcode (9.2)
425424353 The Unarchiver (3.11.3)
409183694 Keynote (7.3.1)
408981434 iMovie (10.1.8)
'''


class TestProject(TestCase):
    @mock.patch('subprocess.check_output')
    def test_installed_packages(self, mock_check_output):
        mock_check_output.return_value = APPS

        apps = [(app_id, app_name) for app_id, app_name in app_store.apps()]
        self.assertEquals(
            apps,
            [
                ('497799835', 'Xcode'),
                ('425424353', 'The Unarchiver'),
                ('409183694', 'Keynote'),
                ('408981434', 'iMovie'),
            ]
        )
