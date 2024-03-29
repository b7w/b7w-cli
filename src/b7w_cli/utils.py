import functools
import os
import shlex
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from time import time

import toml

DEFAULT_CONFIG = """
[Mount]
# name = "smb://user@host/folder"

"""


def timeit(f):
    msg = '# {0} complete in {1:.0f} min {2:.0f} sec ({3:.0f}ms)'

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        try:
            return f(*args, **kwargs)
        finally:
            elapsed = time() - start
            print(msg.format(f.__name__, elapsed // 60, elapsed % 60, elapsed * 1000))

    return wrapper


@contextmanager
def cd(folder):
    current = os.getcwd()
    os.chdir(os.path.expanduser(folder))
    try:
        yield
    finally:
        os.chdir(current)


def read_config():
    p = Path('~/.b7w.ini').expanduser()
    if not p.exists():
        with p.open(mode='w') as f:
            f.write(DEFAULT_CONFIG)

    return toml.load(p)


def iter_files(base_path, pattern='*'):
    base = Path(base_path)
    if base.is_dir():
        for path in base.glob(pattern):
            if path.is_file() and not path.match('.*'):
                yield path
    if base.is_file() and not base.match('.*'):
        yield base


def script(text, with_stdout=True):
    t = shlex.quote(text)
    if with_stdout:
        return os.system(f'osascript -e {t}')
    else:
        return os.system(f'osascript -e {t} > /dev/null')


def notification(title, text):
    script(f'display notification "{text}" with title "{title}"')
