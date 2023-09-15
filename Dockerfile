#############
# FRONT END #
#############
FROM node:bullseye-slim as fe

# Copy files over
WORKDIR /code
COPY . .

# Install required libraries
RUN npm ci --quiet

# Build the front end
RUN npm run build

##################
# DJANGO BUILDER #
##################
FROM python:3.11.4-slim-buster AS builder

# Copy code
WORKDIR /code
COPY . /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install needed libraries
RUN apt-get update && apt-get install -y ca-certificates gcc \
    musl-dev libffi-dev musl-dev g++ npm libpq-dev python-psycopg2

# Install needed libraries, but disable environments
RUN pip install --upgrade pip && pip install --no-input poetry && \
    poetry export --without-hashes --format=requirements.txt > requirements.txt

# build wheel
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/dist -r requirements.txt

###########
# FINAL #
###########
FROM python:3.11.4-slim-buster

RUN apt-get update && apt-get install -y postgresql libpq-dev python-psycopg2

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
WORKDIR /code

COPY --from=builder /code/dist /dist
COPY --from=builder /code/pyproject.toml .
RUN pip install --upgrade pip && pip install --no-cache /dist/*

# Copy project files
COPY . /code

# Copy FE build
COPY --from=fe /code/frontend /code/frontend/
COPY --from=fe /code/frontend/build /code/frontend/build/

# chown all the files to the app user
RUN chown -R app:app /code

RUN python manage.py collectstatic --noinput

# change to the app user
USER app