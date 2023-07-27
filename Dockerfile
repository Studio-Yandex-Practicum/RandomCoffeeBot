FROM python:3.11

RUN python -m pip install --upgrade pip

WORKDIR /app


RUN pip install poetry==1.3.2
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

COPY . .

CMD [ "python", "src/bot/bot.py" ]
