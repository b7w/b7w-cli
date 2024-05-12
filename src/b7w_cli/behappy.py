import configparser
import io
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from dateutil.parser import parse as dateutil_parse


class BeHappyFile:
    def __init__(self, folder: Path):
        self.folder = folder

    def new(self):
        title = self._title()
        date = self._parse_or_now()
        thumbnail = self._first_image()
        config = self._create(title, date, thumbnail)
        buffer = io.StringIO()
        config.write(buffer)

        with Path(self.folder, 'behappy.ini').open(mode='w') as f:
            buffer.seek(0)
            f.write(buffer.read().strip() + '\n')

    def _create(self, title, date, thumbnail):
        config = configparser.ConfigParser()
        config['album'] = dict(id=self._uid(), title=title, description='', date=date, tags='private')
        config['images'] = dict(thumbnail=thumbnail, include='*.jpg', exclude='')
        config['videos'] = dict(include='VIDEO/*.mp4', exclude='')
        return config

    def _title(self):
        try:
            _, value = self.folder.name.split(' - ')
            return value.strip()
        except Exception:
            return ''

    def _parse_or_now(self):
        try:
            value, _ = self.folder.name.split(' - ')
            return dateutil_parse(value.strip()).strftime('%Y-%m-%d')
        except Exception:
            print('# Cannot parse time, set now')
            return datetime.now().strftime('%Y-%m-%d')

    def _first_image(self):
        for i in self.folder.glob('*.jpg'):
            return i.name
        return ''

    def _uid(self):
        return uuid4().hex


def behappy_new():
    folder = Path('.').absolute()
    file = BeHappyFile(folder)
    file.new()
