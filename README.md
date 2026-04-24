# NoteFlow Notes Service

notes-service is the public-facing microservice responsible for handling note-related operations in the NoteFlow project.

It acts as the bridge between authenticated users and the internal persistence layer (`notes-data-service`).

---

## Responsibilities

This service is responsible for:

* validating authenticated users via auth-service
* exposing public note endpoints
* calling notes-data-service for persistence
* enforcing user-level access control

This service is **not responsible for**:

* user registration or login
* password hashing or JWT generation
* direct database access

---

## Role In The Architecture

The application flow is:

```
Client
  -> notes-service
      -> auth-service (/me)
      -> notes-data-service (/internal/notes)
          -> PostgreSQL
```

Within NoteFlow:

* auth-service handles authentication
* notes-service handles public API and access control
* notes-data-service handles persistence

---

## Tech Stack

* Python
* FastAPI
* httpx
* Docker
* pytest

---

## Project Structure

```
app/
├── core/
│   └── config.py
├── dependencies/
│   └── auth.py
├── routers/
│   └── notes.py
├── schemas/
│   └── notes.py
└── main.py

tests/
└── test_notes.py

Dockerfile
requirements.txt
.env.example
```

---

## Environment Variables

Defined in `.env.example`:

```
NOTES_SERVICE_PORT=8002

AUTH_SERVICE_URL=http://127.0.0.1:8001
NOTES_DATA_SERVICE_URL=http://127.0.0.1:8003
```

### Docker on Mac note

If running inside Docker:

```
AUTH_SERVICE_URL=http://host.docker.internal:8001
NOTES_DATA_SERVICE_URL=http://host.docker.internal:8003
```

---

## Running The Service

### Local

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8002
```

Swagger UI:

```
http://127.0.0.1:8002/docs
```

---

### Docker

```
docker build -t noteflow-notes-service .
docker run --rm -p 8002:8002 --env-file .env noteflow-notes-service
```

---

## Health Endpoints

### GET /health

```
{
  "status": "ok",
  "service": "NoteFlow Notes Service",
  "version": "0.1.0"
}
```

---

## Public API Endpoints

All endpoints require:

```
Authorization: Bearer <access_token>
```

---

### GET /notes

Returns notes for the authenticated user.

---

### POST /notes

Creates a new note.

Request:

```
{
  "title": "My note",
  "content": "Example content"
}
```

---

### GET /notes/{note_id}

Returns a specific note.

---

### PUT /notes/{note_id}

Updates a note.

---

### DELETE /notes/{note_id}

Deletes a note.

---

### PATCH /notes/{note_id}/archive

Archives/unarchives a note.

---

### PATCH /notes/{note_id}/pin

Pins/unpins a note.

---

## Authentication Flow

1. Client logs in via auth-service
2. Receives JWT token
3. Sends requests to notes-service with Authorization header
4. notes-service calls:

```
GET /me (auth-service)
```

5. Extracts user_id
6. Calls notes-data-service with user_id

---

## Example Flow

### 1. Login

```
POST http://127.0.0.1:8001/login
```

---

### 2. Create note

```
POST http://127.0.0.1:8002/notes
Authorization: Bearer TOKEN
```

---

### 3. Internal call

notes-service calls:

```
POST /internal/notes
```

with:

```
{
  "user_id": 1,
  "title": "...",
  "content": "..."
}
```

---

## Validation Rules

* token must be valid
* user must exist (validated via auth-service)
* user_id is NEVER taken from request body
* all operations are scoped to authenticated user

---

## Error Behavior

Expected responses:

* 401 Unauthorized → invalid or missing token
* 404 Not Found → note not owned by user
* 422 Unprocessable Entity → invalid request

---

## Manual Testing

Use Swagger:

```
http://127.0.0.1:8002/docs
```

Steps:

1. Login via auth-service
2. Copy token
3. Click "Authorize" in Swagger
4. Test endpoints

---

## Current Status

Current implementation:

* authentication integration completed
* communication with notes-data-service completed
* CRUD endpoints implemented
* user-level access control enforced

---

## Next Step

Next integration point:

* Kong API Gateway
* routing:

  * /auth → auth-service
  * /notes → notes-service

---

## Notes

* notes-service does not access PostgreSQL directly
* all persistence is delegated to notes-data-service
* architecture follows microservice separation of concerns

---
