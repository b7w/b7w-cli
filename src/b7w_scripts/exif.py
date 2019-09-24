import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List

from b7w_scripts.utils import iter_batch, filter_hidden, filter_ext, JPEG_EXT, RAW_EXT


class Exif:
    class Prop:
        def __init__(self, name):
            self.name = name

        def __get__(self, obj: 'Exif', objtype=None):
            if obj is None:
                return self
            return self.fget(obj)

        def fget(self, obj: 'Exif'):
            return obj._raw.get(self.name)

    maker = Prop('Exif:Make')
    model = Prop('Exif:Model')
    lens_model = Prop('Exif:LensModel')
    iso = Prop('Exif:ISO')
    fnumber = Prop('Exif:FNumber')
    exposure_time = Prop('Exif:ExposureTime')
    focal_length = Prop('Exif:FocalLength')
    orientation = Prop('Exif:Orientation')
    style = Prop('MakerNotes:FilmMode')
    datetime_original = Prop('Exif:DateTimeOriginal')

    def __init__(self, raw):
        """
        :type raw: dict
        """
        self.path = Path(raw['SourceFile'])
        self._raw = raw

    @property
    def datetime(self):
        if 'DateTimeOriginal' in self._raw:
            return datetime.strptime(self._raw['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        return None

    def diff(self, other: 'Exif'):
        props = (Exif.maker, Exif.model, Exif.lens_model, Exif.style, Exif.orientation, Exif.datetime_original)
        for p in props:
            self_value = p.fget(self)
            other_value = p.fget(other)
            if self_value != other_value:
                name = p.name.ljust(8, ' ')
                yield f'{name}\t{self_value}\t->\t{other_value}'

    def __eq__(self, other: 'Exif') -> bool:
        props = (
            Exif.maker,
            Exif.model,
            Exif.lens_model,
            Exif.iso,
            Exif.fnumber,
            Exif.exposure_time,
            Exif.focal_length,
            Exif.orientation,
            Exif.style,
            Exif.datetime_original,
        )
        return all(p.fget(self) == p.fget(other) for p in props)


def exiftool(files: List[Path]):
    args = [i.absolute().as_posix() for i in files]
    cmd = 'exiftool -groupNames -json -quiet'.split() + args
    result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').rstrip('\r\n').strip()
    return json.loads(result)


def exiftool_one(file: Path):
    res = exiftool([file])
    return res[0]


def exiftool_update(src: Path, dst: Path, props: List):
    args = ' '.join(props)
    cmd = f'exiftool -tagsfromfile "{src.as_posix()}" -MakerNotes {args} "{dst.as_posix()}"'
    return os.system(cmd)


def read_exif(path):
    for paths in iter_batch(filter_ext(filter_hidden(Path(path).glob('**/*.*')), JPEG_EXT), 64):
        for image in exiftool(paths):
            yield Exif(image)


def fix_exif_from_raw(path, dry_run):
    exif_info = read_exif(path)
    for exif in exif_info:
        p = exif.path
        raw_files = list(filter_ext(Path(p.parent, 'RAW').glob(p.with_suffix('.*').name), RAW_EXT))
        if len(raw_files) > 1:
            print(f'WARN: find more than one RAW file: {raw_files}')
        if len(raw_files) == 1:
            raw_exif = Exif(exiftool_one(raw_files[0]))
            if raw_exif != exif:
                if not dry_run:
                    props = (Exif.maker, Exif.model, Exif.lens_model, Exif.orientation)
                    exiftool_update(raw_exif.path, p, [f'-{i.name}' for i in props])
                yield exif, raw_exif
            else:
                yield exif, None
