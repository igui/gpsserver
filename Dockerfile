FROM python:3.7

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN useradd -m app -G users && chown -R app:app /app
COPY --chown=app:app . .
ENV DB_PATH /app/db/db.sqlite3
RUN mkdir /app/db && chown -R app:app /app/db
USER app
RUN touch /app/db/db.sqlite3
VOLUME [ "/app/db" ]
EXPOSE 8000/tcp
EXPOSE 9000/udp
CMD supervisord