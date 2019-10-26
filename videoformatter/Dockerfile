FROM python:3.7
RUN mkdir /usr/src/videoformatter
WORKDIR /usr/src/videoformatter
COPY ./requirements.txt /usr/src/videoformatter/
RUN pip install  -r requirements.txt
RUN apt-get update -y && apt-get install -y software-properties-common

RUN apt-get -y install ffmpeg