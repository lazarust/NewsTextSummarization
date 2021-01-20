FROM pytorch/pytorch:latest
MAINTAINER Thomas Lazarus (Github: lazarust)

ENV PYTHONUNUNBUFFERED 1

RUN mkdir /newssite
WORKDIR /newssite

RUN apt-get update && \
    apt-get install -y curl \
    git \
    python3-dev \
    python3-pip \
    wget \
    default-jdk \
    default-libmysqlclient-dev \
    mysql-client

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./newssite /newssite
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
