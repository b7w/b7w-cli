import os

from b7w_cli.utils import script, notification


def flush_dns():
    os.system('dscacheutil -flushcache')
    os.system('sudo killall -HUP mDNSResponder')


def mount_volumes(conf: dict):
    try:
        for volume in conf.get('Mount', {}).values():
            print(f'Mount volume "{volume}"')
            script(f'mount volume "{volume}"')
        notification('Remount', 'Ok')
    except Exception as e:
        print(e)
        notification('Remount', f'Error: {e}')
