import subprocess


def packages():
    packages = subprocess.check_output(
        ['brew', 'cask', 'list']
    ).decode('utf8').split('\n')

    for package in packages:
        if package == '':
            continue

        yield package
