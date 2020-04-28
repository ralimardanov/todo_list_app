FROM python:3.7.1


ENV FLASK_APP "app.app.py"
ENV APP_SETTINGS=prod
# DB ENV-ler burda olacag

RUN mkdir /app
WORKDIR /app

COPY . /app

RUN apt-get update -y &&    \
    pip install -r requirements.txt && \
    apt-get install -y postgresql-client

# ADD prestart.sh .
RUN chmod +x prestart.sh
CMD ["/app/prestart.sh"]

EXPOSE 8080

CMD flask run --host=0.0.0.0 --port=8080
