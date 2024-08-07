FROM python:3.10

LABEL maintainer="api"

ENV DEBUG 0
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY requirements-dev.txt /tmp/requirements.dev.txt
COPY ./app /app
COPY ./tests /app/tests
WORKDIR /app
EXPOSE 8000
EXPOSE 8501
EXPOSE 8081

ARG DEV=true

RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get clean && \
    apt-get autoremove -y && \
    pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
