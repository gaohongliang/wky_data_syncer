FROM python:3.6

MAINTAINER Mr Gao

ADD ./src /app
ADD ./requirements.txt /app

# VOLUME ["/app/conf/config.ini"]

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/main.py"]
