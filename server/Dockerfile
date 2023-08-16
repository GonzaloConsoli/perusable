# server/Dockerfile

# pull official base image
FROM python:3.10

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install dependencies
COPY ./requirements.txt .
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
