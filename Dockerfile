FROM python:3.7-alpine

COPY requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "run.py", "--bind", "0.0.0.0", "--port", "8085"]
