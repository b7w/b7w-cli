import shutil
from pathlib import Path

from b7w_cli.cli import organise
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
        assert result.exit_code == 0

    assert list(Path('./tmp').glob('*')) == []
