# TODO RUN AS NON ROOT USER

FROM python:3.11-slim

WORKDIR /src

RUN apt update -y
RUN apt install g++ -y
RUN pip install poetry==1.5.1
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-root

COPY app/weather_api ./app/weather_api
COPY app/setup.py ./app/setup.py
RUN pip install -e app

ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=8080

ENTRYPOINT python app/weather_api/main.py
