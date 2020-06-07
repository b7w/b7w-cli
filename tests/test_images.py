import shutil
import traceback
from pathlib import Path

from b7w_cli.cli import organise, merge
from b7w_cli.utils import cd
from click.testing import CliRunner


def test_organise():
    """
    Invoke img organize in empty folder
    """
    # given
    shutil.rmtree('./tmp', ignore_errors=True)
    Path('./tmp').mkdir()

    with cd('./tmp'):
        runner = CliRunner()
        result = runner.invoke(organise, [])
        print(result.stdout)
        if result.exc_info:
            traceback.print_exception(*result.exc_info)
        assert result.exit_code == 0

    assert list(Path('./tmp').glob('*')) == []


def test_merge():
    """
    Invoke img merge
    """
    # given
    shutil.rmtree('./tmp', ignore_errors=True)
    Path('./tmp/RAW').mkdir(parents=True, exist_ok=True)
    Path(Path.home(), ".Trash").mkdir(parents=False, exist_ok=True)
    for i in range(1, 5):
        Path(f'./tmp/RAW/{i}.RAF').touch()
    Path('./tmp/1.jpg').touch()
    Path('./tmp/3.jpg').touch()

    with cd('./tmp'):
        runner = CliRunner()
        result = runner.invoke(merge, ['--force'])
        print(result.stdout)
        if result.exc_info:
            traceback.print_exception(*result.exc_info)
        assert result.exit_code == 0

        assert sorted(i.as_posix() for i in Path('./').glob('*.jpg')) == ['1.jpg', '3.jpg']
        assert sorted(i.as_posix() for i in Path('./RAW').glob('*')) == ['RAW/1.RAF', 'RAW/3.RAF']
