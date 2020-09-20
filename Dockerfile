FROM python:3.6

MAINTAINER Mr Gao

COPY *.py /app/
COPY conf/config.ini /app/conf/
COPY requirements.txt /app/

WORKDIR /app/

VOLUME ["/app/store"]

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/main.py"]
