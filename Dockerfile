# 1. Use an official Python base image
FROM python:3.11-slim

# 2. Set environment variables
# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures console output is flushed immediately
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory in the container
WORKDIR /app

# 4. Install dependencies
# We copy only the requirements first to leverage Docker's cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the project files into the container
COPY . .

# 6. Run the analysis script
# This will generate the outputs inside the container when it starts
CMD ["python", "pyfiles/analysis.py"]