import os
import boto3
from botocore.exceptions import ClientError
from hurry.filesize import size
from bucket.utils import ProgressPercentage, gzip_stream, should


class CmdParser(object):
    s3 = boto3.resource('s3')
    bucket = None
    bucket_name = None
    here = os.path.abspath(os.path.dirname(__file__))

    def parse(self, cmd):
        command_and_args = cmd.split()
        cmd = command_and_args[0]
        args = command_and_args[1:]
        try:
            getattr(self, cmd)(args)
        except Exception as e:
            print(e)
            self.help()

    def use(self, args):
        """Changes your current bucket. Example: use my-bucket"""
        try:
            assert len(args) > 0
            try:
                self.bucket_name = args[0]
                self.bucket = self.s3.Bucket(self.bucket_name)
                assert self.bucket in self.s3.buckets.all()
                print("Using bucket %s" % self.bucket_name)
            except AssertionError:
                print("Invalid bucket!")
        except AssertionError:
            print("I need a bucket name!")

    def pwd(self, args):
        """Shows which bucket you are using."""
        try:
            assert len(args) == 0
            print('You are using the following bucket: %s' % self.bucket_name)
        except AssertionError:
            print('This command takes no arguments!')

    def dir(self, args):
        try:
            assert len(args) == 0
            print('Available buckets:')
            for bucket in self.s3.buckets.all():
                print('\t%s' % bucket.name)
        except AssertionError:
            print('This command takes no arguments!')

    def ls(self, args):
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
                print('I need a bucket for that!')
        except AssertionError:
            print('This command takes no arguments!')

    def delete(self, args):
        """Deletes a file from your current bucket."""
        try:
            assert len(args) > 0
            file_name = args[0]
            try:
                if should('Delete %s?' % file_name):
                    self.s3.Object(self.bucket_name, file_name).load()
                    self.s3.Object(self.bucket_name, file_name).delete()
                    print('File %s deleted!' % file_name)
            except ClientError:
                print('File %s not found in bucket %s' % (file_name, self.bucket_name))
        except AssertionError:
            print('I need a file name!')

    def down(self, args):
        """Uploads a file to your current bucket. Compression is available (gzip)."""
        try:
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
            print('\n%s downloaded!' % file_name)
        except AssertionError:
            print("Check your arguments!")

    def up(self, args):
        """Uploads a file to your current bucket. Compression is available (gzip)."""
        try:
            assert len(args) > 0
            path = args[0]
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
                print('\n%s uploaded!' % file_name)
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

    @staticmethod
    def help():
        print('AAAAAAAAAAAAAAAA')
