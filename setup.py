from distutils.core import setup

setup(
    name='bucket',
    version='1.0',
    packages=[''],
    url='https://github.com/guitmz/bucket',
    license='Apache License, Version 2.0',
    author='Guilherme Thomazi Bonicontro',
    author_email='thomazi@linux.com',
    description='CLI tool to manage S3 files',
    install_requires=[
        'boto3',
        'hurry.filesize'
    ]
)
