FROM python:3.7
RUN mkdir /usr/src/apiGateway
WORKDIR /usr/src/apiGateway
COPY requirements.txt /usr/src/apiGateway/
RUN pip install  -r requirements.txt
COPY . /usr/src/apiGateway/