# NEAT

This project consists of two parts:
- a backend written in Flask that accepts JSON data and returns PROMETHEE ranking results,
- a simple frontend in HTML/JavaScript that sends data to the backend and displays the results.

## Requirements

### Docker version (easiest)
- Docker
- Docker Compose

### Without Docker
- Python 3.8+
- pip

## Running with Docker Compose

The easiest way to run the whole application is to use Docker Compose.

1. Go to the folder containing the Compose file:
   ```bash
   cd docker
   ```
2. Start the containers:
   ```bash
   docker compose up --build
   ```
3. After startup, the application will be available at the following addresses:
   - frontend: http://localhost:5001
   - backend: http://localhost:5000/parse_json

To stop the application, use:
```bash
docker compose down
```

## Running the backend locally with Python

If you want to run the backend without Docker:

1. Go to the backend folder:
   ```bash
   cd backend
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the application:
   ```bash
   python app.py
   ```
4. The backend will be available at:
   ```text
   http://localhost:5000/parse_json
   ```

## Running the frontend locally

The frontend is a simple static page. You can open it directly in your browser:

```text
frontend/index.html
```

## Project structure

- backend/ contains the Flask API and the PROMETHEE calculation logic.
- frontend/ contains the HTML/JavaScript UI.
- docker/ contains Docker configuration for running both parts together.
- example.json contains a sample input payload with criteria and alternatives.

## Quick start

Once the backend is running, you can open the frontend directly in your browser:

```text
frontend/index.html
```

From there, you can define criteria and alternatives, submit the data, and the application will send it to the backend for processing.

## Backend endpoint

The backend supports the endpoint:
```text
POST /parse_json
```

Example request using curl:
```bash
curl -X POST http://localhost:5000/parse_json -H "Content-Type: application/json" -d '{"example": true}'
```
## Hosted deployment

The application is also hosted here:
- Frontend: http://mcda.pm.szczecin.pl/
- Backend: http://mcda.pm.szczecin.pl/api/v1/neat/parse_json