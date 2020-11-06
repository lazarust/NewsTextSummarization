FROM pytorch/pytorch:latest
MAINTAINER Thomas Lazarus (Github: lazarust)

ENV PYTHONUNUNBUFFERED 1

RUN mkdir /newssite
WORKDIR /newssite

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./newssite /newssite
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
