FROM python:3.13.1-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

#Set PYTHONPATH to include all our code so we can import
#functions between the backend and frontend. 
#This is needed until we develop an API.
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["streamlit", "run", "frontend/app.py", "--server.port=5000"]