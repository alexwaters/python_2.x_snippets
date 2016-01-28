import urllib2


def update_tlds():
    """
    Downloads a list of TLDs from 'source' and stores the TLDs in list 'new_tlds'.
    Compares 'new_tlds' to a local file at 'location', and creates a file there if it does not exist.
    (If you get write errors, it may be due to your file permissions.)
    If there are 'new_tlds' not in 'old_tlds' it will rewrite the file with the current 'new_tlds'
    This could be further expanded with runtime args for print_status, and whether to overwrite the file or just \
    append the diff between the sets.
    """
    try:
        location = '../TLDs.txt'
        source = 'http://data.iana.org/TLD/tlds-alpha-by-domain.txt'
        old_tlds, new_tlds, status = [], [], ''
        print_status = True

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
            with open(location, 'w+') as f:
                for tld in new_tlds:
                    f.write(tld + '\n')
            status += 'Success, list has been updated.\n' + \
                      'TLDs Added: ' + str(list(set(new_tlds)-set(old_tlds))) + '\n'

        if print_status:
            print status

    except Exception as e:
        print e

update_tlds()
