#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Start at the bottom (`if __name__ == '__main__':`) and follow the
# execution from there.

import os
from datetime import datetime, timedelta
from urllib2 import urlopen


def should_update(filename, update_interval):
    """Is `filename`'s mtime more than `update_interval` ago?"""
    if not os.path.isfile(filename):
        return True
    # Working with datetime/timedelta objects usually result in code
    # that is easier to read.
    file_mtime = datetime.fromtimestamp(os.stat(filename).st_mtime)
    return file_mtime + update_interval <= datetime.now()


def download_tlds(url):
    """
    Returns the (stripped) lines from the given URL that are not
    comments.

    The URL is assumed to a be that of a text file (no HTML parsing is
    performed).

    Comment lines start with `#`.
    """
    # This is a separate function in order to isolate any future changes
    # that may be needed when the format of the TLDs list changes. For
    # example, if you want to use the Public Suffix list
    # (https://publicsuffix.org/) format, you only need to change this
    # function:
    #     return [line.strip() for line in urlopen(url)
    #             if line and not line.startswith('//')]
    # The Separation of Concerns principle is at work here.

    # DO use list comprehensions
    return [line.strip() for line in urlopen(url)
            if not line.startswith('#')]


def update_tlds(filename, url, update_interval=None):
    """
    Update the TLDs list in `filename` with the TLDs from `url`, but
    only if after a minimum of `update_interval`.

    :param url: The URL to download the text list of TLDs from.
    :type update_interval: ``datetime.timedelta``
    :returns: ``None`` if no update was attempted (`update_interval` not
        yet reached), or a list of new TLDs.
    """
    if update_interval is None:
        update_interval = timedelta(days=3)

    # This function contains your main algorithm and should be as
    # readable as possible. That implies factoring out any logic that is
    # not strictly part of the main algorithm, into separate functions.
    # A good way to achieve this, is the outside-in approach: Write this
    # function first, as if all other functions that it uses already
    # exist. In that way you will only need to "fill in the gaps"
    # (implement the missing functions), and you already know what the
    # APIs (function signatures in this case) should look like.
    if not should_update(filename, update_interval):
        return

    # The functionality to load the current TLDs from the file was
    # deemed as too simple and very unlikely to change, to justify
    # factoring it out into a separate function. In the end, I believe
    # that the source is easier to understand this way.
    current_tlds = []
    if os.path.isfile(filename):
        current_tlds = [line.strip() for line in open(filename)]
    # The downloading of TLDs, while similarly simple (a single list
    # comprehension), is much more likely to change in implementation.
    # The implementation is, however, not the concern of this algorithm,
    # and is therefore factored out into the `download_tlds()` function.
    url_tlds = download_tlds(url)
    new_tlds = sorted(set(url_tlds) - set(current_tlds))

    if new_tlds:
        # Since the total number of TLDs is not very big and the
        # resulting file is also quite small, we can simply recreate the
        # whole file. Similar to the argument below, it would be better
        # to only append `new_tlds` to the file if the total size of the
        # dataset was sufficiently large.
        with open(filename, 'w') as tldfile:
            # Combine all TLDs into a single (newline separated) string
            # and write it at once, in stead of writing each TLD/line
            # separately.
            # If the list of TLDs was VERY big (millions/billions of
            # lines) and/or each TLD was a bigger data structure, it
            # would have been better to serialise and write each one
            # separately. But in cases of this magnitude it is faster to
            # pass all the data to the operating system, and let it
            # figure out how to perform the low level writing.
            tldfile.write('\n'.join(url_tlds))

    # We only return the new TLDs, since those are the ones most likely
    # to be required outside of this function. The complete updated list
    # is still accessible via the filename that was passed into this
    # function.
    return new_tlds


if __name__ == '__main__':
    # Always put "top-level" code in an `if __name__ == '__main__':`
    # guard. Otherwise it will be executed when you import this file.

    # I used your source of TLDs in this example, but would like you to
    # consider using the Public Suffix list (https://publicsuffix.org/).
    # In most cases that would be the more appropriate list to use.
    # The update interval of 1 second below is only for testing
    # purposes.
    new_tlds = update_tlds(
        'tlds.txt', 'http://data.iana.org/TLD/tlds-alpha-by-domain.txt',
        update_interval=timedelta(seconds=1))

    # User feedback is not part of the `update_tlds()` function's
    # responsibilities, so we give feedback here.
    if new_tlds is None:
        print 'Update not performed'
    elif new_tlds:
        # Use `str.join(iterable)` in stead of `str(list(...))`
        print 'New TLDs: %s' % (', '.join(new_tlds),)
    else:
        # new_tlds must be []
        print 'No new TLDs :('

# Note: There is no error handling in this code. That is not an
# oversight but deliberately done, because any error that occurs in this
# code *should* bubble up, and fail immediately. It is up to the client
# code (the code that uses this module) to check for errors.
# Since the code is separated by concern, the most likely errors (file
# I/O, and downloading of TLDs/network I/O) will not lead to data loss.
