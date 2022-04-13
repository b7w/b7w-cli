import shutil
import time
from itertools import chain
from pathlib import Path

from b7w_cli.utils import iter_files


def organise_ext():
    """
    Rename upper case extensions to lover case
    """
    start = time.time()
    count = 0
    extensions = ('.JPG', '.MOV', '.MP4',)
    files = (i for i in iter_files('.') if i.suffix in extensions)
    for path in files:
        new_name = path.with_suffix(path.suffix.lower())
        path.rename(new_name)
        print('Rename ' + new_name.as_posix())
        count += 1

    elapsed = int(time.time() - start)
    print('# Rename {0} file extensions in {1:d} min {2:d} sec'.format(count, elapsed // 60, elapsed % 60))


def organise_raw():
    """
    Move RAW to sub folder
    """
    start = time.time()
    count = 0
    raw_path = 'RAW'
    extensions = ('.RAF', '.CR2',)
    files = [i for i in iter_files('.') if i.suffix in extensions]
    if not Path(raw_path).exists() and files:
        Path(raw_path).mkdir()
    for f in files:
        f.rename(f.parent / raw_path / f.name)
        print('Move {} '.format(f.name))
        count += 1
    elapsed = int(time.time() - start)
    print('# Move {0} raw files in {1:d} min {2:d} sec'.format(count, elapsed // 60, elapsed % 60))


def organise_video():
    """
    Move video to sub folder
    """
    start = time.time()
    count = 0
    video_path = Path('VIDEO')
    extensions = ('.mov', '.mp4',)
    files = [i for i in iter_files('.') if i.suffix in extensions]
    if not video_path.exists() and files:
        video_path.mkdir()
    for f in files:
        f.rename(f.parent / video_path / f.name)
        print('Move {} '.format(f.name))
        count += 1
    elapsed = int(time.time() - start)
    print('# Move {0} video files in {1:d} min {2:d} sec'.format(count, elapsed // 60, elapsed % 60))


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
                    shutil.move(p, Path.home() / ".Trash" / p.name)
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
