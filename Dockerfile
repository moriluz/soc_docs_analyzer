FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENV OPENAI_API_KEY='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'

RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "soc_analyzer.wsgi:application"]