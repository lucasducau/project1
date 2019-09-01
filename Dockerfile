FROM python:3.6.8

WORKDIR /usr/src/app

RUN apt-get install libpq-dev -y
#RUN apt-get install python-dev -y

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_DEBUG=1
ENV FLASK_APP=application.py
ENV FLASK_ENV=development


CMD ["flask","run"]
