FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Provide a dummy key so collectstatic can run at build time
ENV SECRET_KEY=build-dummy-key-not-used-in-production

RUN mkdir -p /app/staticfiles
RUN python manage.py collectstatic --noinput

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
