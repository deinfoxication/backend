FROM python:3.5-alpine
RUN apk add -U ca-certificates
RUN mkdir -p /deinfoxication /.cache/pip
RUN chown -R 1000 /deinfoxication /.cache/pip
WORKDIR /deinfoxication
ADD requirements.txt /deinfoxication
RUN pip install -r requirements.txt
USER 1000