import functools
from pathlib import Path
from time import time_ns


def timeit(f):
    msg = '# {0} complete in {1:.0f} min {2:.1f} sec ({3}ns)'

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time_ns()
        try:
            return f(*args, **kwargs)
        finally:
            elapsed = time_ns() - start
            elapsed_sec = elapsed / 10 ** 9

            print(msg.format(f.__name__, elapsed_sec // 60, elapsed_sec % 60, elapsed))

    return wrapper


def iter_files(base_path):
    for path in Path(base_path).glob('*'):
        if path.is_file() and not path.match('.*'):
            yield path
