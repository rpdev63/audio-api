FROM python:3.11

# Set a directory for the app
WORKDIR /usr/src/fastapi_app

# Copy all the files to the container
COPY . .

# Install dependencies
RUN apt-get update
# RUN apt-get install -y libsndfile1 ffmpeg
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Tell the port number the container should expose
EXPOSE 8000

# Run the command
CMD ["uvicorn", "api:app"]