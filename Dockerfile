# alpine 3.13 is the last version with python 3.8
FROM alpine:3.13

RUN apk add --no-cache \
        py3-asn1crypto \
        py3-certifi \
        py3-cffi \
        py3-click \
        py3-cryptography \
        py3-cparser \
        py3-dotenv \
        py3-future \
        py3-h11 \
        py3-idna \
        py3-pip \
        py3-six \
        py3-sniffio \
        py3-tornado \
 && pip install python-telegram-bot==12.1.1

COPY . /app
WORKDIR /app

EXPOSE 8085
CMD ["python3", "run.py", "--bind", "0.0.0.0", "--port", "8085"]
