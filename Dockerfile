FROM python:3.11

# Set a directory for the app
WORKDIR /api

# Copy all the files to the container
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose a non-privileged port
EXPOSE 8080

# Use an environment variable for the port
ENV PORT=8080

# Run the command with the configurable port
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "${PORT}"]