FROM python:3.11

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install poetry==1.3.2
RUN poetry config virtualenvs.create false
RUN poetry install --without dev
