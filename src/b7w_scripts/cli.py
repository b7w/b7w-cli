import click as click

from b7w_scripts.exif import fix_exif_from_raw
from b7w_scripts.utils import timeit


@click.group()
def cli():
    pass


@click.group()
def exif():
    pass


@exif.command()
@click.option('--path', default='.', help='path')
@click.option('--raw-path', default='RAW', help='RAW folder path')
@click.option('--dry-run', default=False, is_flag=True, help='Do not apply changes')
@timeit
def fix(path, raw_path, dry_run):
    """
    Find original RAW file for JPEG and copy EXIF if needed
    """
    c_all, c_fixed = 0, 0
    data = fix_exif_from_raw(path, dry_run)
    for img_exif, raw_exif in data:
        if raw_exif:
            e = '\n\t'.join(img_exif.diff(raw_exif))
            print(f'File: {img_exif.path}\n\t{e}')
            c_fixed += 1
        else:
            c_all += 1

    print(f'# Found {c_all} pairs, fix {c_fixed} images')


def main():
    cli.add_command(exif)
    cli()


if __name__ == '__main__':
    main()
