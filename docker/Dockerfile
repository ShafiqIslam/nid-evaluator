FROM python:3.7-slim

ARG APP_PORT

RUN apt-get clean && apt-get -y update && apt-get -y install python3-dev \
    && apt-get -y install build-essential  python-opencv tesseract-ocr

RUN mkdir -p /usr/src/app && cd /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
COPY ./traind_data/* /usr/share/tesseract-ocr/4.00/tessdata/

RUN pip install -r requirements.txt --src=/usr/local/src

EXPOSE ${APP_PORT}

CMD gunicorn -w ${WORKER} -b ${APP_HOST}:${APP_PORT} run:wsgi --reload --timeout=300
