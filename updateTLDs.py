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
    """
    try:
        old_tlds, new_tlds, status = [], [], ''

        for tld in urllib2.urlopen(url):
            if '#' not in tld:
                new_tlds.append(tld.strip('\n'))

        with open(filename, 'a+') as f:
            f.seek(0)
            for line in f:
                if '#' not in line:
                    old_tlds.append(line.strip('\n'))

        if old_tlds == new_tlds:
            status = '%sSuccess, list is current.\n' % status
        else:
            with open(filename, 'w+') as ff:
                for tld in new_tlds:
                    ff.write(tld + '\n')
            status = '%sSuccess, list has been updated.\n' % status
            status = '%sTLDs Added: %s\n' % (
                status, ', '.join(sorted(set(new_tlds) - set(old_tlds))))
    except Exception as e:
        status = e

    return status


if __name__ == '__main__':
    day = 86400  # one day = 86,400 seconds
    run_every = day * 3
    filename = 'TLDs.txt'
    url = 'http://data.iana.org/TLD/tlds-alpha-by-domain.txt'

    if not os.path.isfile(filename):
        update_tlds(filename, url)
    else:
        file_mod_time = os.stat(filename).st_mtime
        time_elapsed = time.time() - file_mod_time

        if time_elapsed > run_every:
            print update_tlds(filename, url)
        else:
            print 'TLDs last updated about %s days ago.' % (
                str(round((time_elapsed/day), 2)))
