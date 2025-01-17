#Normally I'd use alpine for smaller image sizes but it doesn't work well with streamlit
FROM python:3.13.1-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

RUN python -m unittest discover -s tests

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]