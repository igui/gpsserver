FROM python:3.7

WORKDIR /app
# Necessary for collect static to work since we don't have a SECRET_KEY yet
ENV SECRET_KEY=dummy_key
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN useradd -m app -G users && chown -R app:app /app
COPY --chown=app:app . .
ENV DB_PATH /app/db/db.sqlite3
RUN mkdir -p /app/db && chown -R app:app /app/db
USER app
RUN touch /app/db/db.sqlite3 && ./manage.py collectstatic --noinput
VOLUME [ "/app/db" ]
EXPOSE 8000/tcp
EXPOSE 9000/udp
CMD supervisord

