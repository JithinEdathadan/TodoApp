# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /TodoApp

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Set environment variable (optional)
ENV PYTHONPATH=/app

# Run with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["fastapi", "dev", "app/main.py"]
