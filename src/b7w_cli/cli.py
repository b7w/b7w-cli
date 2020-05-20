import click

from b7w_cli.images import organise_ext, organise_raw, organise_video
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


if __name__ == '__main__':
    main()
