FROM python:3.7.2-alpine

WORKDIR /DataAnalyticsToolkit

ADD . /DataAnalyticsToolkit

RUN python setup.py install

ENTRYPOINT flask run -h 0.0.0.0 -p 80
