FROM python:alpine

MAINTAINER Guilherme Thomazi Bonicontro <thomazi@linux.com>

ADD . /bucket

WORKDIR /bucket

RUN python setup.py install

CMD ["bucket"]
