FROM python:3.10.0-alpine
WORKDIR /app
COPY ./requirements.txt ./requirements-dev.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt
COPY . .
CMD python
