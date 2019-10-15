FROM python:3.7

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN useradd -m app -G users && chown -R app:app /app
COPY . .
USER app
EXPOSE 8000/tcp
EXPOSE 9000/udp
CMD supervisord