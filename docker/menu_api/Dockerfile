FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app/main.py /code/main.py
COPY ./app/db_requests.py /code/db_requests.py
COPY ./app/settings.env /code/settings.env

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install opentracing-instrumentation
RUN pip install --upgrade "setuptools>=29" "pip>=9"

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5433"]
