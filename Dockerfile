FROM python:3.8-slim

# Set application name
ARG APP_NAME=clarity

RUN mkdir -p /root/${APP_NAME}/
WORKDIR /root/${APP_NAME}/
COPY . /root/${APP_NAME}/

# Install poetry
RUN pip install poetry
# Install deps
RUN poetry config virtualenvs.create false \
  && poetry install

WORKDIR /root/${APP_NAME}/

# Logic to cache busting test stage
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

RUN pytest -vv --disable-warnings --cov=src

