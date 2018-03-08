import os
import shutil
import tempfile
from unittest import TestCase, mock

from collectors import brew


DEPS = b'''
a:
b: c
c: d
d: 
f:
g:
'''

PACKAGE_INFO = b'''
ffmpeg: stable 3.4.2 (bottled), HEAD
Play, record, convert, and stream audio and video
https://ffmpeg.org/
/usr/local/Cellar/ffmpeg/3.4.2 (248 files, 51.1MB) *
  Built from source on 2018-03-06 at 18:35:40 with: --with-x265 --with-fdk-aac
From: https://github.com/Homebrew/homebrew-core/blob/master/Formula/ffmpeg.rb
==> Dependencies
Build: nasm, pkg-config, texi2html
Recommended: lame, x264, xvid
Optional: chromaprint, fdk-aac
==> Options
--with-chromaprint
	Enable the Chromaprint audio fingerprinting library
--with-fdk-aac'''


class TestProject(TestCase):
    @mock.patch('subprocess.check_output')
    def test_installed_packages(self, mock_check_output):
        mock_check_output.return_value = DEPS

        packages = [package for package in brew._installed_packages()]
        self.assertEquals(packages, ['a', 'b', 'f', 'g'])

    @mock.patch('subprocess.check_output')
    def test_get_install_options(self, mock_check_output):
        mock_check_output.return_value = PACKAGE_INFO

        self.assertEquals(brew._get_install_options('ffmpeg'), ['--with-x265', '--with-fdk-aac'])
