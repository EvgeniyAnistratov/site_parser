FROM python:3.8.1-alpine

COPY ./requirements.txt ./requirements-dev.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . .

CMD python
