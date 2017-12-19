import os
import sys
import shutil
import argparse
import subprocess


def rebuild_dotfiles(github_url, local_path):
    _init(os.path.join(local_path, 'scripts'))
    _brew(os.path.join(local_path, 'scripts'))
    _brew_cask(os.path.join(local_path, 'scripts'))
    _app_store(os.path.join(local_path, 'scripts'))

    _dotfiles(os.path.join(local_path, 'dotfiles'))


def _init(script_root):
    if not os.path.exists(script_root):
        os.makedirs(script_root)
    
    with open(os.path.join(script_root, 'init'), 'w') as fp:
        fp.write('#!/usr/bin/env bash\n\n')
        fp.write('xcode-select --install\n')
        fp.write('read -p "Press any key to continue... " -n1 -s\n\n')
        fp.write('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"\n')


def _brew(script_root):
    packages = subprocess.check_output(['brew', 'leaves']).decode('utf8').split('\n')
    with open(os.path.join(script_root, 'brew'), 'w') as fp:
        fp.write('#!/usr/bin/env bash\n\n')
        for package in packages:
            fp.write(f'brew install {package}\n')


def _brew_cask(script_root):
    packages = subprocess.check_output(['brew', 'cask', 'list']).decode('utf8').split('\n')
    with open(os.path.join(script_root, 'brew_cask'), 'w') as fp:
        fp.write('#!/usr/bin/env bash\n\n')
        for package in packages:
            if package == '':
                continue

            fp.write(f'brew cask install {package}\n')


def _app_store(script_root):
    installed_apps = subprocess.check_output(['mas', 'list']).decode('utf8').split('\n')
    with open(os.path.join(script_root, 'app_store'), 'w') as fp:
        fp.write('#!/usr/bin/env bash\n\n')
        for installed_app in installed_apps:
            if installed_app == '':
                continue

            app_id = installed_app.split(' ')[0]
            app_name = ' '.join(installed_app.split(' ')[1:-1])
            fp.write(f'# install {app_name}\n')
            fp.write(f'mas install {app_id}\n\n')

    
def _dotfiles(dotfiles_root):
    home = os.path.expanduser("~")
    shutil.copy(os.path.join(home, '.bash_profile'), os.path.join(dotfiles_root, '.bash_profile'))


def _parse_args():
    parser = argparse.ArgumentParser(prog='autodot')

    parser.add_argument('github_url')
    parser.add_argument('local_path')

    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()

    rebuild_dotfiles(args.github_url, args.local_path)
