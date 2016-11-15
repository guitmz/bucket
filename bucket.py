#!/usr/bin/python
import boto3
import gzip
import os
from botocore.exceptions import ClientError
from cmd import Cmd
from io import BytesIO


class BucketPrompt(Cmd):
    s3 = boto3.resource('s3')
    bucket = None
    bucket_name = None

    def do_use(self, args):
        """Changes your current bucket."""
        try:
            assert len(args) > 0
            try:
                self.bucket_name = args
                self.bucket = self.s3.Bucket(self.bucket_name)
                assert self.bucket in self.s3.buckets.all()
                print("Using bucket %s" % self.bucket_name)
            except AssertionError:
                print("Invalid bucket!")
        except AssertionError:
            print("I need a bucket name!")

    def do_pwd(self, args):
        """Shows which bucket you are using."""
        try:
            assert len(args) == 0
            print('You are using the following bucket: %s' % self.bucket_name)
        except AssertionError:
            print('This command takes no arguments!')

    def do_up(self, args):
        """Uploads a file to your current bucket."""
        try:
            assert len(args) > 0
            path = args
            compress = self.should_compress_file()
            self.upload_file(path, compress)
        except AssertionError:
            print("I need a file name!")

    @staticmethod
    def gzip_stream(file):
        gz_stream = BytesIO()
        with gzip.GzipFile(fileobj=gz_stream, mode='wb') as gzf:
            gzf.write(file.read())
        gz_stream.seek(0)
        return gz_stream

    def upload_file(self, path, compress):
        basename = os.path.basename(path)
        try:
            with open(path, 'rb') as f:
                if compress:
                    gz_file = self.gzip_stream(f)
                    compressed_file = basename + '.gz'
                    self.s3.Object(self.bucket_name, compressed_file).put(Body=gz_file)
                    print('%s uploaded!' % compressed_file)
                else:
                    self.s3.Object(self.bucket_name, basename).put(Body=f)
                    print('%s uploaded!' % basename)
        except FileNotFoundError:
            print('File %s not found!' % path)

    def do_del(self, args):
        """Deletes a file from your current bucket."""
        try:
            assert len(args) > 0
            file_name = args
            try:
                self.s3.Object(self.bucket_name, file_name).load()
                self.s3.Object(self.bucket_name, file_name).delete()
                print('File %s deleted!' % file_name)
            except ClientError:
                print('File %s not found in bucket %s' % (file_name, self.bucket_name))
        except AssertionError:
            print("I need a file name!")

    def do_ls(self, args):
        """List files and folders in your current bucket."""
        try:
            assert len(args) == 0
            try:
                assert self.bucket is not None
                for obj in self.bucket.objects.all():
                    print(obj.bucket_name, obj.key)
            except AssertionError:
                print('I need a bucket!')
        except AssertionError:
            print('This command takes no arguments!')

    @staticmethod
    def do_quit(args):
        """Quits the program."""
        try:
            assert len(args) == 0
            print("¯\_(ツ)_/¯")
            raise SystemExit
        except AssertionError:
            print('This command takes no arguments!')

    @staticmethod
    def should_compress_file():
        while True:
            user_input = input('Compress file? [y/n]: ')
            if user_input in ['y', 'Y']:
                return True
            elif user_input in ['n', 'N']:
                return False


if __name__ == '__main__':
    prompt = BucketPrompt()
    prompt.prompt = '>_ '
    prompt.cmdloop('Starting prompt...')
