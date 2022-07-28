import os
import shlex
import time
from itertools import chain
from typing import List

from b7w_cli.utils import iter_files


def convert_mov2mp4(paths: List[str], preview: int, preset: str, quality: int, rotate: int):
    """
    Rename upper case extensions to lover case
    """
    paths = paths if paths else ('',)
    start = time.time()
    count = 0
    files = chain.from_iterable(iter_files(p, pattern='**/*.mov') for p in paths)
    for path in files:
        src = path.as_posix()
        dst_video = path.with_suffix('.mp4')
        dst_video_path = dst_video.as_posix()
        dst_preview = path.with_suffix('.jpg')
        dst_preview_path = dst_preview.as_posix()
        if not dst_video.exists():
            print(f'Converting {src} to {dst_video_path}')
            cmd = f'nice -n 10' \
                  f' HandBrakeCLI -i {src} -o {dst_video_path}' \
                  f' --preset={shlex.quote(preset)}' \
                  f' --crop="0:0:0:0" --quality={quality} --rotate="angle={rotate}:hflip=0"'
            if os.system(cmd) == 0:
                count += 1

        print(f'Creating thumbnail {src} to {dst_preview_path}')
        if dst_preview.exists():
            dst_preview.unlink()
        cmd = f'ffmpeg -i {src} -vframes 1 -an -ss {preview} {dst_preview_path}'
        os.system(cmd)
        cmd = f'exiftool -overwrite_original -TagsFromFile {src} "-EXIF:all>EXIF:all" {dst_preview_path}'
        os.system(cmd)
        cmd = f'exiftool -overwrite_original -TagsFromFile {src} "-EXIF:DateTimeOriginal>DateTimeOriginal" {dst_video_path}'
        os.system(cmd)

    elapsed = int(time.time() - start)
    print('# Convert {0} videos in {1:d} min {2:d} sec'.format(count, elapsed // 60, elapsed % 60))
