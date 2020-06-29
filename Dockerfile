FROM python:3.7.2-alpine as base

FROM base as builder

RUN mkdir /DataAnalyticsToolkit
WORKDIR /DataAnalyticsToolkit

RUN python setup.py install

FROM base

ADD . /DataAnalyticsToolkit
WORKDIR /DataAnalyticsToolkit

ENTRYPOINT flask run -h 0.0.0.0 -p 80
