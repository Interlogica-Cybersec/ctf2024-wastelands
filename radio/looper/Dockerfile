FROM python:3.10.14-alpine3.19
RUN apk add alpine-sdk
COPY app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY app/ /app
CMD python3 -BOu mclient.py