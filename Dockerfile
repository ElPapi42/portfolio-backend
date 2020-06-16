FROM python:3.8.3-slim
LABEL maintainer="Whitman Bohorquez"

RUN mkdir portfolio && cd portfolio

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY / /
RUN python setup.py install

CMD [ "uvicorn", "portfolio.asgi:application", "--reload" ]
