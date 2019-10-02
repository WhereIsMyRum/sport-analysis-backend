FROM python:3.7
RUN mkdir /usr/src/vidapp
WORKDIR /usr/src/vidapp
COPY ./requirements.txt /usr/src/vidapp/
RUN pip install  -r requirements.txt
COPY . /usr/src/vidapp/