FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin libsqlite3-mod-spatialite postgis postgresql-postgis

COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

EXPOSE 8000

COPY app/src /app/

RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "PAC.wsgi:application", "--bind", "0.0.0.0:8000"]