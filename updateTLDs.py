import time, urllib2, os.path
"""
This should update the TLDs list every few days if you plug this into your main application. There may be some variance in time.time()
and system local timezones (unsure, didn't test). Also maybe some issues with st_mtime depending on your operating system.
"""


# one day = 86,400 seconds
day = 86400
run_every = day*3
loc = 'TLDs.txt'
src = 'http://data.iana.org/TLD/tlds-alpha-by-domain.txt'
start_time = time.time()


def update_tlds(location, source):
    """
    Downloads a list of TLDs from 'source' and stores the TLDs in list 'new_tlds'.
    Compares 'new_tlds' to a local file at 'location', and creates a file there if it does not exist.
    (If you get write errors, it may be due to your file permissions.)
    If there are 'new_tlds' not in 'old_tlds' it will rewrite the file with the current 'new_tlds'
    This could be further expanded with runtime args for print_status, and whether to overwrite the file or just \
    append the diff between the sets.
    :param location: the location of the local file
    :param source: the location of the remote file
    """
    try:
        old_tlds, new_tlds, status = [], [], ''

        for tld in urllib2.urlopen(source):
            if '#' not in tld:
                new_tlds.append(tld.strip('\n'))

        with open(location, 'a+') as f:
            f.seek(0)
            for line in f:
                if '#' not in line:
                    old_tlds.append(line.strip('\n'))

        if old_tlds == new_tlds:
            status += 'Success, list is current.\n'
        else:
            with open(location, 'w+') as ff:
                for tld in new_tlds:
                    ff.write(tld + '\n')
            status += 'Success, list has been updated.\n' + \
                      'TLDs Added: ' + str(list(set(new_tlds)-set(old_tlds))) + '\n'

    except Exception as e:
        status = e

    return status


if not os.path.isfile(loc):
    update_tlds(loc, src)

file_mod_time = os.stat(loc).st_mtime
time_elapsed = time.time() - file_mod_time

if time_elapsed > run_every:
    updated = update_tlds(loc, src)
    print updated
else:
    print "TLDs last updated about " + str(round((time_elapsed/day), 2)) + " days ago."
