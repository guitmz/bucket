from codecs import open
from os.path import abspath, dirname, join
from setuptools import find_packages, setup

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='bucket',
    version='1.0',
    url='https://github.com/guitmz/bucket',
    license='Apache License, Version 2.0',
    author='Guilherme Thomazi Bonicontro',
    author_email='thomazi@linux.com',
    description='CLI tool to manage S3 files',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='cli',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'boto3',
        'hurry.filesize',
        'prompt_toolkit'
    ],
    entry_points={
        'console_scripts': [
            'bucket=bucket.cli:main',
        ],
    },
)
