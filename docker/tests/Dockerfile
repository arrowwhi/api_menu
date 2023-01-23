FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# COPY ./app/requests_class.py /code/requests_class.py
# COPY ./app/tests_menu_api.py /code/tests_menu_api.py
# COPY ./app/consts.py /code/consts.py
# COPY ./app/pytest.ini /code/pytest.ini

COPY ./app/main.py /code/main.py


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install opentracing-instrumentation
RUN pip install --upgrade "setuptools>=29" "pip>=9"

COPY ./app /code/app

# CMD ["pytest","tests_menu_api.py"]
CMD ["python","main.py"]