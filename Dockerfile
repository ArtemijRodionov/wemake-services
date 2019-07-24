FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
WORKDIR /usr/code

COPY requirements.txt .
RUN apk update \
    # add psycopg2 deps
    && apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev \
    && pip install -r requirements.txt \
    && apk del .build-deps \
    && adduser -D test_assignment
USER test_assignment

COPY . .
CMD ./run.sh
