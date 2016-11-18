import gzip
import threading
from io import BytesIO
from hurry.filesize import size as sz
import sys


def should(msg):
    while True:
        user_input = input('%s [y/n]: ' % msg)
        if user_input in ['y', 'Y']:
            return True
        elif user_input in ['n', 'N']:
            return False


def gzip_stream(file):
    gz_stream = BytesIO()
    with gzip.GzipFile(fileobj=gz_stream, mode='wb') as gzf:
        gzf.write(file.read())
    gz_stream.seek(0)
    return gz_stream


# Borrowed from boto3 docs with a minor tweak in how it displays the sizes.
class ProgressPercentage(object):
    def __init__(self, filename, size):
        self._filename = filename
        self._size = float(size)
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write("\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, sz(self._seen_so_far), sz(self._size),
                    percentage))
            sys.stdout.flush()
