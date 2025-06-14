FROM python:3.11-slim

# Install system dependencies (for mysqlclient, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Set environment variables (can be overridden by Heroku)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port for Heroku
EXPOSE 5000

# Launch app using gunicorn (recommended for Heroku)
# Replace run:app with your correct entry point, e.g., app.py => app:app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
