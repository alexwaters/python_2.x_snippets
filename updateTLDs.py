"""
This should update the TLDs list every few days if you plug this into
your main application. There may be some variance in time.time() and
system local timezones (unsure, didn't test). Also maybe some issues
with st_mtime depending on your operating system.
"""

import time
import urllib2
import os.path


def update_tlds(filename, url):
    """
    Downloads a list of TLDs from 'url' and stores the TLDs in list
    'new_tlds'.

    Compares 'new_tlds' to a local file at 'filename', and creates a
    file there if it does not exist.  (If you get write errors, it may
    be due to your file permissions.) If there are 'new_tlds' not in
    'old_tlds' it will rewrite the file with the current 'new_tlds'.

    :param filename: the location of the local file
    :param url: the location of the remote file
    :return: List of TLDs that were added to the file.
    """
    try:
        old_tlds = []
        new_tlds = [tld.strip('\n') for tld in urllib2.urlopen(url)
                    if '#' not in tld]
        if os.path.isfile(filename):
            old_tlds = [line.strip('\n') for line in open(filename)
                        if '#' not in line]

        if old_tlds == new_tlds:
            return []
        else:
            with open(filename, 'w') as f:
                for tld in new_tlds:
                    f.write(tld + '\n')
            return sorted(set(new_tlds) - set(old_tlds))
    except Exception as e:
        return e


if __name__ == '__main__':
    day = 86400  # one day = 86,400 seconds
    run_every = day * 3
    filename = 'TLDs.txt'
    url = 'http://data.iana.org/TLD/tlds-alpha-by-domain.txt'

    delta_mtime = 0
    if os.path.isfile(filename):
        delta_mtime = time.time() - os.stat(filename).st_mtime

    if delta_mtime < run_every:
        print 'TLDs last updated about %s days ago.' % (
            round(delta_mtime / day, 2))

    tlds = update_tlds(filename, url)
    if isinstance(tlds, Exception):
        print 'Error: %r' % tlds
        exit(1)
    elif not tlds:
        print 'Success, list is current.'
    else:
        print 'Success, list has been updated.'
        print 'TLDs Added: %s' % ', '.join(tlds)
