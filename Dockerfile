# Use a minimal Python image
FROM python:3.12-slim

# Ensure Python output is sent straight to logs
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (Docker cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that Gunicorn will serve on
EXPOSE 8000

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

