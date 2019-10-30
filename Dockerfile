FROM python:3.7

WORKDIR /app
# Necessary for collect static to work since we don't have a SECRET_KEY yet
ENV SECRET_KEY=dummy_key
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -m app -G users && chown -R app:app /app
COPY --chown=app:app . .
USER app
CMD supervisord

