import functools
from time import time_ns

JPEG_EXT = '.jpg .jpeg'.split()
RAW_EXT = '.crw .cr2 .cr3 .raf .nef .nrw'.split()
ALL_EXT = JPEG_EXT + RAW_EXT


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


def iter_batch(iterable, size):
    buf = []
    for it in iterable:
        buf.append(it)
        if len(buf) == size:
            yield buf
            buf = []
    if buf:
        yield buf


def filter_hidden(iterable):
    for path in iterable:
        if not path.name.startswith('.'):
            yield path


def filter_ext(iterable, extensions):
    for path in iterable:
        if path.suffix.lower() in extensions:
            yield path
