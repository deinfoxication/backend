FROM python:3.5
RUN apt-get update && apt-get install ca-certificates libpq-dev -y
RUN adduser --system --no-create-home --disabled-login --uid 1000 deinfoxication
RUN mkdir -p /deinfoxication /.cache/pip
RUN chown -R deinfoxication /deinfoxication /.cache/pip
WORKDIR /deinfoxication
ADD requirements.txt /deinfoxication
RUN pip install -r requirements.txt
USER deinfoxication
ADD . /deinfoxication
