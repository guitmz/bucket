# bucket
An interactive shell to manage files in AWS S3 written in Python 3.


Bucket is a CLI to list, upload and delete (more to come!) files in a AWS S3 bucket. There are other tools available and I but I wanted a interactive one.

# Requirements
Only `boto3` and `hurry.filesize` are required, along with, of course, your AWS credentials in `~/.aws/credentials` file.

# Usage
To start using your bucket: 

`>_ use my-bucket`

To list files in bucket (it will list your available buckets if you haven't ran the above command yet): 

`>_ ls`

To upload a file (you will be asked if you want to compress it before uploading, resulting in a gzip file): 

`>_ up /path/to/your/file`

To delete a file:

`>_ del file.ext`

# Usage video
[![asciicast](https://asciinema.org/a/ci8ew38fuyqpbcsln4bc2a2le.png)](https://asciinema.org/a/ci8ew38fuyqpbcsln4bc2a2le)
