FROM python:3.7-slim

MAINTAINER @tonmoy <shtonmoy007@gmail.com>
ARG APP_PORT
# INSTALL REQUIRED LIBRARIES FOR PYTHON
RUN apt-get clean && apt-get -y update && apt-get -y install python3-dev \
    && apt-get -y install build-essential  python-opencv tesseract-ocr
#CREATE APP DIRECTORY AND COPY SOURCES TO APP DIRECTORY AND MAKE THE DIRECTORY AS BASH ENTRY POINT
RUN mkdir -p /usr/src/app && cd /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
COPY ./traind_data/* /usr/share/tesseract-ocr/4.00/tessdata/
# INSTALL PROJECT REQUIREMENTS AND SET TIMEZONE
RUN pip install -r requirements.txt --src=/usr/local/src

EXPOSE ${APP_PORT}

CMD gunicorn -w ${WORKER} -b ${APP_HOST}:${APP_PORT} run:wsgi --reload