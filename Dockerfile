FROM python:3.9
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock /src/
RUN pip install pipenv
RUN pipenv install --system
