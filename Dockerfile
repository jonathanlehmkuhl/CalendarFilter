FROM python:3.11.7-slim

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]