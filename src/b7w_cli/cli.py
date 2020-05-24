import click

from b7w_cli.images import organise_ext, organise_raw, organise_video
from b7w_cli.mac import flush_dns
from b7w_cli.utils import timeit


@click.group()
def main():
    pass


@main.group()
def img():
    pass


@img.command()
@timeit
def organise():
    organise_ext()
    organise_raw()
    organise_video()


@main.group()
def mac():
    pass


@mac.command()
@timeit
def flush():
    flush_dns()


if __name__ == '__main__':
    main()
