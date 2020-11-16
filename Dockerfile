FROM pytorch/pytorch:latest
MAINTAINER Thomas Lazarus (Github: lazarust)

ENV PYTHONUNUNBUFFERED 1

RUN mkdir /newssite
WORKDIR /newssite

RUN apt-get update && \
    apt-get install -y curl \
    wget \
    default-jdk

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ENV PORT=8000
EXPOSE 8000

COPY ./newssite /newssite
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
