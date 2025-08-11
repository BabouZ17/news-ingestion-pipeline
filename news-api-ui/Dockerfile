FROM python:3.12-slim

ARG PORT=8000

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["streamlit", "run", "main.py", "--server.port", $PORT, "--server.address=0.0.0.0"]
