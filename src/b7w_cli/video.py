import os
import shlex
import time
from itertools import chain
from typing import List

from b7w_cli.utils import iter_files


def convert_mov2mp4(paths: List[str], preset: str, quality: int, rotate: int):
    """
    Rename upper case extensions to lover case
    """
    paths = paths if paths else ('',)
    start = time.time()
    count = 0
    files = chain.from_iterable(iter_files(p, pattern='**/*.mov') for p in paths)
    for path in files:
        input = path.as_posix()
        output = path.with_suffix('.mp4').as_posix()
        print(f'Converting {input} to {output}')
        cmd = f'nice -n 10' \
              f' HandBrakeCLI -i {input} -o {output}' \
              f' --preset={shlex.quote(preset)}' \
              f' --crop="0:0:0:0" --quality={quality} --rotate="angle={rotate}:hflip=0"'
        if os.system(cmd) == 0:
            count += 1

    elapsed = int(time.time() - start)
    print('# Convert {0} videos in {1:d} min {2:d} sec'.format(count, elapsed // 60, elapsed % 60))
