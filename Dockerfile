FROM python:3.9.16-slim-buster

WORKDIR /app

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements-docker.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
COPY . .

CMD python3 app.py