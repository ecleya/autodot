import subprocess


def apps():
    installed_apps = subprocess.check_output(
        ['mas', 'list']
    ).decode('utf8').split('\n')

    for installed_app in installed_apps:
        if installed_app == '':
            continue

        app_id = installed_app.split(' ')[0]
        app_name = ' '.join(installed_app.split(' ')[1:-1])
        yield app_id, app_name
