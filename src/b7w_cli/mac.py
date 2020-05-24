import os


def flush_dns():
    os.system('dscacheutil -flushcache')
    os.system('sudo killall -HUP mDNSResponder')
