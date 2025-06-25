# FastAPI Pet Store Mock Server

This is a FastAPI implementation of the Pet Store API specification that provides mock responses instead of using httpbin.org.

## Features

- **List Pets**: GET `/get` - List all pets with optional filtering by status and limit
- **Get Pet by ID**: GET `/get?petId={id}` - Get specific pet information
- **Create Pet**: POST `/post` - Create a new pet
- **Health Check**: GET `/health` - Server health status
- **Debug Endpoint**: GET `/pets` - View all pets in the database

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Use FastAPI's built-in server:
```bash
fastapi run main.py --host 0.0.0.0 --port 8080
```

The server will start on `http://localhost:8080`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8080/docs
- **ReDoc documentation**: http://localhost:8080/redoc
- **OpenAPI JSON**: http://localhost:8080/openapi.json

## Example Usage

### List all pets
```bash
curl http://localhost:8080/get
```

### List pets with limit
```bash
curl "http://localhost:8080/get?limit=3"
```

### Filter pets by status
```bash
curl "http://localhost:8080/get?status=available"
```

### Get specific pet
```bash
curl "http://localhost:8080/get?petId=1"
```

### Create a new pet
```bash
curl -X POST http://localhost:8080/post \
  -H "Content-Type: application/json" \
  -d '{"name": "Fluffy", "tag": "cat"}'
```

## Sample Data

The server comes pre-loaded with 5 sample pets:
- Buddy (dog, available)
- Whiskers (cat, available)
- Polly (parrot, sold)
- Goldie (fish, pending)
- Rex (dog, available)

## Notes

- This is a demo server with in-memory storage
- Data is reset when the server restarts
- All responses are mock data that mimics httpbin.org format
- No actual database operations are performed
- Uses FastAPI's built-in server (no uvicorn required) 