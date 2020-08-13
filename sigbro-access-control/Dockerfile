FROM python:3.8.2-slim

LABEL maintainer "scor2k <scor2k@gmail.com>"

# let the container know that there is no tty
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/app
WORKDIR /opt/app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . . 
RUN pip install -e .

CMD [ "/bin/bash", "loop.sh" ] 
