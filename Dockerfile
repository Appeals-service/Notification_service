FROM python:3.13.1-alpine

WORKDIR /opt

RUN apk update
RUN pip install --upgrade pip

COPY ./poetry.lock ./pyproject.toml ./

RUN yes | pip install --no-cache-dir poetry==1.8.3 && \
	poetry config virtualenvs.create false && \
	poetry install --only main --no-interaction --no-ansi

COPY ./src src

CMD ["python", "src/main.py"]
