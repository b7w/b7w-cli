import os

from b7w_cli.utils import script, notification


def flush_dns():
    os.system('dscacheutil -flushcache')
    os.system('sudo killall -HUP mDNSResponder')


def mount_volumes():
    try:
        script('mount volume "smb://test@media.lc/test"')
        notification('Remount', 'Ok')
    except Exception as e:
        print(e)
        notification('Remount', f'Error: {e}')
