FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false \
    UVICORN_RELOAD=false
WORKDIR /code
RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry install --without dev --no-root
COPY weather_api/ /code/weather_api/

RUN groupadd -r fastapi && useradd -r -g fastapi fastapi
RUN chown -R fastapi:fastapi /code

USER fastapi

CMD ["python", "-m", "weather_api"]
