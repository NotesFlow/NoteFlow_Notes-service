# NoteFlow Notes Service

Public notes microservice for the NoteFlow project.

This service connects the authenticated user from `auth-service` with note persistence from `notes-data-service`.

## Responsibilities

This service is responsible for:

- exposing public note endpoints
- validating bearer tokens by calling `auth-service /me`
- extracting the authenticated `user_id`
- calling `notes-data-service` with that `user_id`
- keeping clients away from internal `/internal/notes` endpoints

This service is not responsible for:

- registration or login
- password hashing
- JWT generation
- direct PostgreSQL access
- creating the notes table

## Architecture Flow

```text
Client
  -> notes-service
      -> auth-service /me
      -> notes-data-service /internal/notes
          -> PostgreSQL
```

## Tech Stack

- Python 3.10
- FastAPI
- httpx
- Uvicorn
- pytest

## Environment Variables

Create `.env` from `.env.example`.

Local non-Docker example:

```env
NOTES_SERVICE_PORT=8002
AUTH_SERVICE_URL=http://127.0.0.1:8001
NOTES_DATA_SERVICE_URL=http://127.0.0.1:8003
```

Docker on Mac example, when auth-service and notes-data-service are exposed on the host:

```env
AUTH_SERVICE_URL=http://host.docker.internal:8001
NOTES_DATA_SERVICE_URL=http://host.docker.internal:8003
```

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8002
```

Swagger UI:

```text
http://127.0.0.1:8002/docs
```

## Docker

```bash
docker build -t noteflow-notes-service .
docker run --rm -p 8002:8002 --env-file .env noteflow-notes-service
```

## Public API Endpoints

All `/notes` endpoints require:

```http
Authorization: Bearer <access_token>
```

### GET /health

Checks whether the service is running.

### GET /notes

Lists the authenticated user's notes.

### POST /notes

Creates a note for the authenticated user.

Request body:

```json
{
  "title": "My note",
  "content": "Example content"
}
```

### PUT /notes/{note_id}

Updates a note owned by the authenticated user.

```json
{
  "title": "Updated title",
  "content": "Updated content"
}
```

### DELETE /notes/{note_id}

Deletes a note owned by the authenticated user.

### PATCH /notes/{note_id}/archive

```json
{
  "is_archived": true
}
```

### PATCH /notes/{note_id}/pin

```json
{
  "is_pinned": true
}
```

## Manual Demo

1. Start PostgreSQL.
2. Start `auth-service` on port `8001`.
3. Start `notes-data-service` on port `8003`.
4. Start this service on port `8002`.
5. Register and login through `auth-service`.
6. Use the returned JWT against this service:

```bash
curl -X POST http://127.0.0.1:8002/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN_HERE" \
  -d '{"title":"First public note","content":"Created through notes-service"}'
```

Then list notes:

```bash
curl http://127.0.0.1:8002/notes \
  -H "Authorization: Bearer TOKEN_HERE"
```

## Current Status

Implemented:

- FastAPI bootstrap
- auth-service token validation
- notes-data-service HTTP client
- public CRUD endpoints
- archive endpoint
- pin endpoint
- Docker support
