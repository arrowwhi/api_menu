FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app/main.py /code/main.py



RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install opentracing-instrumentation
RUN pip install --upgrade "setuptools>=29" "pip>=9"

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "5001"]
