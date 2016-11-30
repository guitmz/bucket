FROM python:alpine
MAINTAINER Guilherme Thomazi Bonicontro <thomazi@linux.com>

ADD . /bucket
RUN python bucket/setup.py install \
    && rm -rf bucket

CMD ["bucket"]
