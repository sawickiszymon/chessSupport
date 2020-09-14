FROM python:3.6-alpine

RUN apk update
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt /

RUN pip install -r /requirements.txt
COPY . /app

WORKDIR /app

EXPOSE 5000

CMD ["flask", "run"]