FROM python:3.10

LABEL maintainer="api"

ENV DEBUG 0
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y postgresql-client

COPY requirements.txt /tmp/requirements.txt
COPY requirements-dev.txt /tmp/requirements.dev.txt
COPY ./app /app
COPY ./tests /app/tests
WORKDIR /app

EXPOSE 8081

ARG DEV=true

RUN pip install --upgrade pip && \ 
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then pip install --no-cache-dir -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp 

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8081"]

