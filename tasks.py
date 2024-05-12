from pathlib import Path

from invoke import task, Context

GLOBAL_PIP = '/usr/local/bin/pip3.11'


@task()
def install_local(c: Context):
    *_, last = Path('.').glob('dist/*.whl')
    print('## Building')
    c.run('poetry build')

    print('## Installing')
    c.run(f'{GLOBAL_PIP} install -U --force-reinstall {last.as_posix()}')
