import subprocess


def packages():
    for package in _installed_packages():
        yield package, _get_install_options(package)


def _installed_packages():
    packages = subprocess.check_output(
        ['brew', 'deps', '--installed', '--include-build', '--include-optional']
    ).decode('utf8').split('\n')

    installed_packages = []
    dependencies = set()
    for package in packages:
        if package == '':
            continue

        name, deps = package.split(':')
        installed_packages.append(name)
        dependencies.update(deps.split(' '))

    for installed_package in installed_packages:
        if installed_package in dependencies:
            continue

        yield installed_package


def _get_install_options(package):
    output = subprocess.check_output(
        ['brew', 'info', package]
    ).decode('utf8')
    options = []
    for line in output.split('\n'):
        if 'Built from source on' not in line:
            continue
        
        options = line.split('with: ')[1].split(' ')

    return options
