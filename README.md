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
- [API.md](API.md) describes the input and output JSON structure of the backend API.


## Backend endpoint

The backend supports the endpoint:
```text
POST /parse_json
```

Example request using curl:
```bash
curl --location --request POST 'http://localhost:5000/parse_json' \
--header 'Content-Type: application/json' \
--data-raw '{
  "criteria": [
    {
      "id": "c1",
      "weight": "very high",
      "direction": "max",
      "preference_function": "u-shaped",
      "indifference_threshold": 5,
      "preference_threshold": null,
      "gaussian_threshold": null
    },
    {
      "id": "c2",
      "weight": "medium high",
      "direction": "max",
      "preference_function": "gaussian",
      "indifference_threshold": null,
      "preference_threshold": null,
      "gaussian_threshold": 5
    }
  ],
  "alternatives": [
    {
      "id": "a2",
      "parameters": {
        "c1": {
          "L": 1,
          "A": 2,
          "B": 3,
          "R": 4
        },
        "c2": {
          "L": 1,
          "A": 2,
          "B": 3,
          "R": 4
        }
      }
    },
    {
      "id": "a1",
      "parameters": {
        "c1": {
          "L": 5,
          "A": 6,
          "B": 7,
          "R": 8
        },
        "c2": {
          "L": 5,
          "A": 6,
          "B": 7,
          "R": 8
        }
      }
    }
  ]
}'
```
## Hosted deployment

The application is also hosted here:
- Frontend: http://mcda.pm.szczecin.pl/
- Backend: http://mcda.pm.szczecin.pl/api/v1/neat/parse_json