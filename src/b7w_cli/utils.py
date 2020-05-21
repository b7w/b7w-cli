import functools
import os
from contextlib import contextmanager
from pathlib import Path
from time import time


def timeit(f):
    msg = '# {0} complete in {1:.0f} min {2:.1f} sec ({3}ms)'

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        try:
            return f(*args, **kwargs)
        finally:
            elapsed = time() - start
            elapsed_sec = elapsed / 10 ** 6

            print(msg.format(f.__name__, elapsed_sec // 60, elapsed_sec % 60, round(elapsed * 1000)))

    return wrapper


def iter_files(base_path):
    for path in Path(base_path).glob('*'):
        if path.is_file() and not path.match('.*'):
            yield path


@contextmanager
def cd(folder):
    current = os.getcwd()
    os.chdir(os.path.expanduser(folder))
    try:
        yield
    finally:
        os.chdir(current)
