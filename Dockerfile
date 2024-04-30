FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1 
EXPOSE 8000 
WORKDIR /usr/src/api
COPY . .
RUN pip install -r requirements.txt 

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]