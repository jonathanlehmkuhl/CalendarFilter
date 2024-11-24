FROM python:3.11.7-slim

WORKDIR /app

COPY requirements.txt .requirements.txt

RUN pip install -r requirements.txt

COPY server/ .

EXPOSE 5000

ENV FLASK_APP=server.py
ENV FLASK_ENV=production

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]