FROM python:3.7.1


ENV FLASK_APP "app.app.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True
ENV APP_SETTINGS=dev
# DB ENV-ler burda olacag

RUN mkdir /app
WORKDIR /app

COPY . /app

RUN apt-get update -y &&    \
    pip install -r requirements.txt && \
    apt-get install -y postgresql-client

# ADD prestart.sh .
# RUN prestart.sh

EXPOSE 8080

CMD flask run --host=0.0.0.0 --port=8080