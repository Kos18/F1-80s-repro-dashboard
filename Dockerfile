FROM python:3.12.4-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data ./data
COPY src ./src
COPY app ./app
COPY tests ./tests

EXPOSE 8501

# Streamlit needs to listen on all interfaces inside Docker
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
