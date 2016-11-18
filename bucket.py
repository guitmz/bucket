#!/usr/bin/python

import boto3
import os
from botocore.exceptions import ClientError
from cmd import Cmd
from hurry.filesize import size
from utils import gzip_stream, should, ProgressPercentage


class BucketPrompt(Cmd):
    s3 = boto3.resource('s3')
    bucket = None
    bucket_name = None
    here = os.path.abspath(os.path.dirname(__file__))

    def do_use(self, args):
        """Changes your current bucket. Example: use my-bucket"""
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

    def do_down(self, args):
        """Uploads a file to your current bucket. Compression is available (gzip)."""
        try:
            args = args.split()
            assert len(args) == 2
            file_name = args[0]
            destination_path = args[1]
            file_size = self.s3.ObjectSummary(self.bucket_name, file_name).size
            with open(destination_path, 'wb') as data:
                self.bucket.download_fileobj(
                    file_name,
                    data,
                    Callback=ProgressPercentage(
                        file_name,
                        file_size
                    )
                )
        except AssertionError:
            print("Check your arguments!")

    def do_up(self, args):
        """Uploads a file to your current bucket. Compression is available (gzip)."""
        try:
            assert len(args) > 0
            path = args
            compress = should('Compress file?')
            self.prepare_upload(path, compress)
        except AssertionError:
            print("I need a file name!")

    def prepare_upload(self, path, compress):
        try:
            with open(path, 'rb') as f:
                file_name = os.path.basename(path)
                if compress:
                    gz_file = gzip_stream(f)
                    file_name += '.gz'
                    file_size = gz_file.getbuffer().nbytes
                    self.upload_file(gz_file, file_name, file_size)
                else:
                    file_size = os.path.getsize(path)
                    self.upload_file(f, file_name, file_size)
                print('%s uploaded!' % file_name)
        except FileNotFoundError:
            print('File %s not found!' % path)

    def upload_file(self, file, file_name, file_size):
        self.bucket.upload_fileobj(
            file,
            file_name,
            Callback=ProgressPercentage(
                file_name,
                file_size
            )
        )

    def do_del(self, args):
        """Deletes a file from your current bucket."""
        try:
            assert len(args) > 0
            file_name = args
            try:
                if should('Delete %s?' % file_name):
                    self.s3.Object(self.bucket_name, file_name).load()
                    self.s3.Object(self.bucket_name, file_name).delete()
                    print('File %s deleted!' % file_name)
            except ClientError:
                print('File %s not found in bucket %s' % (file_name, self.bucket_name))
        except AssertionError:
            print('I need a file name!')

    def do_ls(self, args):
        """List files and folders in your current bucket. If no bucket is selected, lists available buckets instead."""
        try:
            assert len(args) == 0
            try:
                assert self.bucket is not None
                for obj in self.bucket.objects.all():
                    print('\t%8s %8s %8s %8s' % (
                        obj.last_modified,
                        obj.owner['DisplayName'],
                        size(obj.size),
                        obj.key
                    ))
            except AssertionError:
                for bucket in self.s3.buckets.all():
                    print('\t%s' % bucket.name)
        except AssertionError:
            print('This command takes no arguments!')

    @staticmethod
    def do_quit(args):
        """Quits the program."""
        try:
            assert len(args) == 0
            print('Bye! ¯\_(ツ)_/¯')
            raise SystemExit
        except AssertionError:
            print('This command takes no arguments!')


if __name__ == '__main__':
    prompt = BucketPrompt()
    prompt.prompt = '>_ '
    try:
        prompt.cmdloop('Starting prompt...')
    except KeyboardInterrupt:
        raise SystemExit
