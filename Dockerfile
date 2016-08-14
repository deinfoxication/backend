FROM python:3.5-alpine
RUN apk add -U ca-certificates
RUN adduser -D -s /bin/false -H -u 1000 deinfoxication
RUN mkdir -p /deinfoxication /.cache/pip
RUN chown -R deinfoxication /deinfoxication /.cache/pip
WORKDIR /deinfoxication
ADD requirements.txt /deinfoxication
RUN pip install -r requirements.txt
USER deinfoxication
