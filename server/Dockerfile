FROM python:3.10.6

WORKDIR /app

RUN pip install --upgrade pip

ADD ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt