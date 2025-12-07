# Base image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy requirements file into container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire messaging app project into the container
COPY . /app/

# Expose Django port
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

