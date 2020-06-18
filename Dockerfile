FROM python:3.8.3-slim
LABEL maintainer="Whitman Bohorquez"

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python setup.py install

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8000", "--reload", "portfolio.wsgi" ]
