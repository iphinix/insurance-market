FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /insura
COPY insura/requirements.txt /insura/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY insura /insura