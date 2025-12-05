# Dockerfile

# 1. Base Image: Use the official Python slim image for a smaller size.
FROM python:3.11-slim

# 2. Environment Variable: Set the standard port for Cloud Run.
ENV PORT 8080

# 3. Working Directory: Set the working directory inside the container.
WORKDIR /app

# 4. Copy Dependencies: Copy the requirements file into the container.
# This step is cached, speeding up future builds if dependencies don't change.
COPY requirements.txt .

# 5. Install Dependencies: Install all necessary Python libraries.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Source Code: Copy the rest of the application code (main.py, etc.) into the container.
COPY . .

# 7. Execution Command: Define the command to run the server when the container starts.
# Uvicorn serves the 'app' object from 'main.py' on all interfaces (0.0.0.0).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]