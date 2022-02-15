FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY insura/requirements.txt /code/
COPY .env /
RUN pip install -r requirements.txt
