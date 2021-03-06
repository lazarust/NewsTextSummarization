FROM pytorch/pytorch:latest
MAINTAINER Thomas Lazarus (Github: lazarust)

ENV PYTHONUNUNBUFFERED 1

RUN mkdir /newssite
WORKDIR /newssite
# TODO: Some of these probably aren't necessary. Remove them. 
RUN apt-get update && \
    apt-get install -y curl \
    git \
    python3-dev \
    python3-pip \
    wget \
    default-jdk \
    default-libmysqlclient-dev \
    mysql-client

COPY requirements.txt ./
RUN pip install -r /requirements.txt

COPY . .
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
