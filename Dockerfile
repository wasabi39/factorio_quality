FROM python:3.13.1-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#~~Set PYTHONPATH to include all our code so we can import~~
#~~functions between the backend and frontend.~~ 
#~~This is needed until we develop an API.~~ 
#TODO look into removing this now that API works 
#(might require a bit of refactoring in other files)
ENV PYTHONPATH=/app

ENV RUNNING_THROUGH_DOCKER=1

RUN python -m unittest discover -s tests

EXPOSE 5000

CMD ["streamlit", "run", "frontend/app.py", "--server.port=5000"]