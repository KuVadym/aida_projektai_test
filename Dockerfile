FROM python:3.10-slim

# off .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# consol log
ENV PYTHONUNBUFFERED 1 


WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "events.wsgi:application", "--bind", "0.0.0.0:8000"]