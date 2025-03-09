import os
import time
from itertools import chain
from pathlib import Path

from b7w_cli.utils import iter_files, script


def organise_ext(base_path):
    """
    Rename upper case extensions to lover case
    """
    start = time.time()
    count = 0
    extensions = ('.JPG', '.MOV', '.MP4',)
    files = (i for i in iter_files(base_path, pattern='**/*') if i.suffix in extensions)
    for path in files:
        new_name = path.with_suffix(path.suffix.lower())
        path.rename(new_name)
        print('[{0}] Rename {1} '.format(base_path, new_name.as_posix()))
        count += 1

    elapsed = int(time.time() - start)
    print('# [{0}] Rename {1} file extensions in {2:d} min {3:d} sec'.format(base_path, count, elapsed // 60,
                                                                             elapsed % 60))


def organise_raw(base_path):
    """
    Move RAW to sub folder
    """
    start = time.time()
    count = 0
    raw_path = Path(base_path, 'RAW')
    extensions = ('.RAF', '.CR2',)
    files = [i for i in iter_files(base_path) if i.suffix in extensions]
    if not raw_path.exists() and files:
        raw_path.mkdir()
    for f in files:
        f.rename(raw_path / f.name)
        print('[{0}] Move {1} '.format(base_path, f.name))
        count += 1
    elapsed = int(time.time() - start)
    print('# [{0}] Move {1} raw files in {2:d} min {3:d} sec'.format(base_path, count, elapsed // 60, elapsed % 60))


def organise_video(base_path):
    """
    Move video to sub folder
    """
    start = time.time()
    count = 0
    video_path = Path(base_path, 'VIDEO')
    extensions = ('.mov', '.mp4',)
    files = [i for i in iter_files(base_path) if i.suffix in extensions]
    if not video_path.exists() and files:
        video_path.mkdir()
    for f in files:
        f.rename(video_path / f.name)
        print('[{0}] Move {1} '.format(base_path, f.name))
        count += 1
    elapsed = int(time.time() - start)
    print('# [{0}] Move {1} video files in {2:d} min {3:d} sec'.format(base_path, count, elapsed // 60, elapsed % 60))


def merge_raws(force=False):
    start = time.time()
    raw_path = 'RAW'
    jpgs = {i.stem for i in iter_files('.')}
    raws = {i.stem for i in iter_files(raw_path)}
    diff = (raws - jpgs)
    moved = []
    if len(diff):
        print('Diff: ' + ', '.join(sorted(diff)))
        answer = 'y' if force else input('Are you sure to move to trash {} photos?(y/n): '.format(len(diff)))
        if answer == 'y':
            for raw_name in diff:
                paths = Path(raw_path).glob(raw_name + '.*')
                for p in paths:
                    code = script(f'tell app "Finder" to move (the POSIX file "{p.absolute().as_posix()}") to trash',
                                  with_stdout=False)
                    if code != 0:
                        print(f'# Finder return {code} exit code, removing file {p.name}')
                        p.unlink()
                    moved.append(p.name)
            print('Moved: ' + ', '.join(moved))
        else:
            print('Stop')
    else:
        print('No difference')
    elapsed = int(time.time() - start)
    print('# Move {0} raw files in {1:d} min {2:d} sec'.format(len(moved), elapsed // 60, elapsed % 60))
    print('# Total {0} images'.format(len(jpgs)))


def jpg_size(paths):
    count = 0
    total = 0
    paths = paths if paths else ('',)

    for f in chain.from_iterable(iter_files(p, pattern='**/*.jpg') for p in paths):
        count += 1
        total += f.stat().st_size
    average = total / count
    t = round(total / 10 ** 6)
    a = round(average / 10 ** 6)
    print(f'Count:\t\t{count}')
    print(f'Total size:\t{t}mb')
    print(f'Average size:\t{a}mb')


def open_all(paths):
    paths = paths if paths else ('',)

    iterable = chain.from_iterable(iter_files(p, pattern='**/*.jpg') for p in paths)
    files = list(sorted(iterable, key=lambda x: x.name))
    count = len(files)
    args = ' '.join(i.as_posix() for i in files)
    print(f'Count:\t\t{count}')
    if count:
        os.system(f'open {args}')
    else:
        print('No files')
