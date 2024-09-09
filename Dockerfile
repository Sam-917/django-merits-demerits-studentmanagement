FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .  

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "schoolstudentmanangment.wsgi.application"]