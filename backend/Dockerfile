# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Run migrations, seed data, and start gunicorn
CMD ["sh", "-c", "python manage.py migrate && python seed_data.py && gunicorn terrasync_backend.wsgi:application --bind 0.0.0.0:$PORT"]
