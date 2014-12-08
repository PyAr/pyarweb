from fabric.api import env, run, task
from fabric.context_managers import cd
from fabric.contrib.console import confirm

env.hosts = ['python.org.ar']
env.user = 'www-pyar'
env.project_path = '/home/www-pyar/pyarweb_beta/pyarweb/'
env.venv_path = '/home/www-pyar/pyarweb_beta/pyarweb_venv/'
env.pip_bin = '%sbin/pip' % (env.venv_path)
env.python_bin = '%sbin/python' % (env.venv_path)
env.gunicorn_bin = '%sbin/gunicorn' % (env.venv_path)


@task
def deploy():
    """Deploy de PyArweb en beta.python.org.ar."""
    git_pull()
    if confirm("Install/upgrade requirements with pip?"):
        install_requeriments()
    django_command('migrate')
    django_command('collectstatic')
    restart()

@task
def restart():
    """Restart gunicorn sending HUP signal to his pid."""
    run('kill -HUP $(cat /tmp/pyar_web.pid)')


def git_pull():
    with cd(env.project_path):
        run('git pull')


def django_command(command):
    with cd(env.project_path):
        run('%s manage.py %s --noinput' % (env.python_bin, command))


def install_requeriments():
    with cd(env.project_path):
        run('%s install --upgrade -r requirements.txt' % (env.pip_bin))
