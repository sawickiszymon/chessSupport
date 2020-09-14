FROM python:3.6-alpine AS builder

RUN apk update
# missing c++ compiler for numpy
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt /

RUN pip install -r /requirements.txt
COPY . /app

WORKDIR /app

# copy the content of the local src directory to the working directory
CMD ["python", "app.py"]