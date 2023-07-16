FROM python:3.10-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ENV FLASK_APP=src/main.py
ENV FLASK_DEBUG=1

COPY . .

WORKDIR .

EXPOSE 8000

RUN chmod +x gunicorn.sh

ENTRYPOINT ["./gunicorn.sh"]