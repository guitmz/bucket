import boto3
from bucket.const import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class S3Resource(object):
    def __init__(self):
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            self.resource = boto3.resource(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
        else:
            self.resource = boto3.resource('s3')
