FROM python:3.11-slim

RUN apt-get update \
    && apt-get upgrade --yes

RUN mkdir /bot
COPY . /bot

WORKDIR /bot

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD [ "python", "app.py" ]