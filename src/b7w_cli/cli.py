import click

from b7w_cli.behappy import behappy_new
from b7w_cli.images import organise_ext, organise_raw, organise_video, merge_raws, jpg_size, open_all
from b7w_cli.mac import flush_dns, mount_volumes
from b7w_cli.utils import timeit, read_config
from b7w_cli.video import convert_mov2mp4


@click.group()
def main():
    pass


@main.group()
def img():
    pass


@img.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True, file_okay=False))
@timeit
def organise(paths):
    for path in paths or ('.',):
        organise_ext(path)
        organise_raw(path)
        organise_video(path)


@img.command()
@click.option('--force', is_flag=True, default=False, help='Do not confirm')
@timeit
def merge(force):
    merge_raws(force)


@img.command()
@click.argument('paths', nargs=-1)
@timeit
def size(paths):
    jpg_size(paths)


@img.command()
@click.argument('paths', nargs=-1)
@timeit
def open(paths):
    open_all(paths)


@main.group()
def video():
    pass


@video.command()
@click.argument('paths', nargs=-1)
@click.option('--preview', default=0, type=int, help='Preview time in seconds')
@click.option('--preset', default='Creator 2160p60 4K',
              help='HandBrake preset, default "Creator 2160p60 4K"')
@click.option('--quality', default=10, type=int, help='Video quality, default 10')
@click.option('--quality', default=20, type=int, help='Video quality, default 20')
@click.option('--rotate', default=0, type=int, help='Video rotation, default 0')
@timeit
def mov_to_mp4(paths, preview, preset, quality, rotate):
    convert_mov2mp4(paths, preview, preset, quality, rotate)


@main.group()
def behappy():
    pass


@behappy.command()
def new():
    behappy_new()


@main.group()
def mac():
    pass


@mac.command()
@timeit
def flush():
    flush_dns()


@mac.command()
@timeit
def mount():
    conf = read_config()
    mount_volumes(conf)


@main.command()
def version():
    from . import __version__
    conf = read_config()
    print(f'Version: {__version__}')
    print(f'Config: {conf}')


if __name__ == '__main__':
    main()
