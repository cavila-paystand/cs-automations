FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY wsgi.py .
COPY app.py .

# Create directory for secrets
RUN mkdir -p /etc/secrets

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "wsgi:app"] 