import gzip
from io import BytesIO


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
