FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "soc_analyzer.wsgi:application"]