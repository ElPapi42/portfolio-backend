FROM python:3.8.3-slim
LABEL maintainer="Whitman Bohorquez"

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python setup.py install

ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "portfolio", "--reload-dir", "api", "portfolio.asgi:application" ]
