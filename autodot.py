import os
import sys
import yaml
import shutil
import argparse
import subprocess

from collectors import brew
from collectors import brew_cask
from collectors import app_store


def rebuild_dotfiles(github_url, local_path):
    settings = yaml.load(open(os.path.join(local_path, '.autodot.yml')))
    _init(os.path.join(local_path, 'scripts'), settings)
    _brew(os.path.join(local_path, 'scripts'))
    _brew_cask(os.path.join(local_path, 'scripts'))
    _app_store(os.path.join(local_path, 'scripts'), settings.get('login_items', []))

    _dotfiles(os.path.join(local_path, 'dotfiles'), settings.get('dotfiles', []))


def _init(script_root, settings):
    if not os.path.exists(script_root):
        os.makedirs(script_root)

    with open(os.path.join(script_root, '../bootstrap.sh'), 'w') as fp:
        fp.write('#!/usr/bin/env bash\n\n')
        fp.write('source ./scripts/init\n')
        if settings.get('brew', False):
            fp.write('source ./scripts/brew\n')
        if settings.get('brew_cask', False):
            fp.write('source ./scripts/brew_cask\n')
        if settings.get('app_store', False):
            fp.write('source ./scripts/app_store\n')
        if settings.get('preferences', False):
            fp.write('source ./scripts/preferences\n')

        fp.write('\n')
        for dotfile in settings.get('dotfiles', []):
            fp.write(f'cp ./dotfiles/{dotfile} ~/{dotfile}\n')
    
    with open(os.path.join(script_root, 'init'), 'w') as fp:
        fp.write('#!/usr/bin/env bash\n\n')
        fp.write('xcode-select --install\n')
        fp.write('read -p "Press any key to continue... " -n1 -s\n\n')
        fp.write('sudo xcodebuild -license accept\n')
        fp.write('read -p "Press any key to continue... " -n1 -s\n\n')
        fp.write('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"\n')


def _brew(script_root):
    with open(os.path.join(script_root, 'brew'), 'w') as fp:
        fp.write('#!/usr/bin/env bash\n\n')
        for package, options in brew.packages():
            fp.write(f'brew install {package} {" ".join(options)}\n')


def _brew_cask(script_root):
    with open(os.path.join(script_root, 'brew_cask'), 'w') as fp:
        fp.write('#!/usr/bin/env bash\n\n')
        for package in brew_cask.packages():
            fp.write(f'brew cask install {package}\n')


def _app_store(script_root, login_items):
    with open(os.path.join(script_root, 'app_store'), 'w') as fp:
        fp.write('#!/usr/bin/env bash\n\n')
        for app_id, app_name in app_store.apps():
            fp.write(f'# install {app_name}\n')
            fp.write(f'mas install {app_id}\n\n')
        
        for login_item in login_items:
            fp.write(f"osascript -e 'tell application \"System Events\" to make login item at end with properties {{name: \"{login_item}\", path:\"/Applications/{login_item}.app\", hidden:false}}'\n")

    
def _dotfiles(dotfiles_root, dotfiles):
    home = os.path.expanduser("~")
    for dotfile in dotfiles:
        shutil.copy(os.path.join(home, dotfile), os.path.join(dotfiles_root, dotfile))


def _parse_args():
    parser = argparse.ArgumentParser(prog='autodot')

    parser.add_argument('github_url')
    parser.add_argument('local_path')

    return parser.parse_args()


def main():
    args = _parse_args()

    rebuild_dotfiles(args.github_url, args.local_path)


if __name__ == '__main__':
    main()
