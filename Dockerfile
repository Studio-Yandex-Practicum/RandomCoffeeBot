FROM python:3.11

RUN mkdir /app

WORKDIR /app
RUN mkdir logs

COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . .
RUN pip install .

CMD [ "python", "src/run.py" ]
