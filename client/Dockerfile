FROM python:3.10-alpine3.15
EXPOSE 80

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["python3", "user_script.py"]