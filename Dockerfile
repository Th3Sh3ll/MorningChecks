FROM python:alpine3.19

COPY . /morningchecks

WORKDIR /morningchecks

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./startApp.sh"]