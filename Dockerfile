FROM python:3.7-slim-stretch
MAINTAINER Thomas Lazarus (Github: lazarust)

ENV PYTHONUNUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /newssite
WORKDIR /newssite
COPY ./newssite /newssite
