import os
import time

from b7w_cli.utils import iter_files


def convert_mov2mp4(preset, quality):
    """
    Rename upper case extensions to lover case
    """
    start = time.time()
    count = 0
    extensions = ('.mov',)
    files = (i for i in iter_files('.') if i.suffix in extensions)
    for path in files:
        input = path.as_posix()
        output = path.with_suffix('.mp4').as_posix()
        print(f'Converting {input} to {output}')
        cmd = f'nice -n 10' \
              f' HandBrakeCLI -i {input} -o {output}' \
              f' --preset="{preset}"' \
              f' --crop="0:0:0:0" --rotate="angle=180:hflip=0" --quality={quality}'
        if os.system(cmd) == 0:
            count += 1

    elapsed = int(time.time() - start)
    print('# Convert {0} videos in {1:d} min {2:d} sec'.format(count, elapsed // 60, elapsed % 60))
