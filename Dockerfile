FROM python:3.5
RUN apt-get update && apt-get install ca-certificates libpq-dev strace lsof net-tools -y
RUN adduser --system --disabled-login --uid 1000 deinfoxication
RUN mkdir -p /deinfoxication /.cache/pip /pip-src
RUN chown -R deinfoxication /deinfoxication /.cache/pip  /pip-src
WORKDIR /deinfoxication
ADD requirements.txt /deinfoxication
RUN pip install --src  /pip-src -r requirements.txt
USER deinfoxication
ADD . /deinfoxication
# This is kinda hack because default src is workdir/src and when we mount a volume on
# development it gets overriten
ENV PYTHONPATH  /pip-src
