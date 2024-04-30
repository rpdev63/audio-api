# Urban Sound Recognition API

This repository contains the source code for the API used by the [Urban Wave Tagger](https://github.com/rpdev63/urban-wav-tagger) application. This API is responsible for processing and recognizing urban sounds using a machine learning model trained on the UrbanSound8k dataset.

## Technology Stack

- **Python**: The API is written in Python, offering robust and versatile programming capabilities.
- **FastAPI**: Utilizes FastAPI framework for high performance and easy-to-manage APIs.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need to have Python installed on your machine. Python 3.8 or higher is recommended. If you intend to use Docker for deployment, Docker needs to be installed as well.

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/rpdev63/audio-api.git
   cd audio-api
   ```

2. **Set up a Virtual Environment (Optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the API**
   ```bash
   uvicorn main:app --reload  # The command assumes your FastAPI app is created in a file called main.py and your FastAPI instance is named app
   ```

### Using Docker

1. **Build the Docker Image**
   ```bash
   docker build -t urban-sound-api .
   ```

2. **Run the Docker Container**
   ```bash
   docker run -p 8000:8000 urban-sound-api
   ```

This will start the API on port 8000, and you can access it at `http://localhost:8000`.

## Documentation

Once the API is running, you can visit `http://localhost:8000/docs` to view the automatically generated Swagger documentation provided by FastAPI. This documentation will allow you to see all endpoints and interact with the API directly from your browser.