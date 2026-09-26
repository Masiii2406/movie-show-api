# Movies & TV Shows API

A REST API server for a hand-crafted catalog of movies and TV shows, built for assignment
**ITCC 14 – Build Your Own API Server Challenge**.

- **Niche:** Movies and TV Shows
- **Stack:** Flask (Python) + SQLite
- **Data:** 20 hand-crafted movies/TV shows (title, year, type, genre, rating, creator)

## Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd movie-tv-api

# 2. Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server (also creates and seeds movies.db on first run)
python3 app.py
```

The server starts at `http://127.0.0.1:5000`.

## Data Model

| Field   | Type    | Required | Notes                                  |
|---------|---------|----------|-----------------------------------------|
| id      | integer | auto     | assigned by the server                  |
| title   | string  | yes      | name of the movie/show                  |
| year    | integer | yes      | release year (or season year)           |
| type    | string  | yes      | must be `"movie"` or `"tv"`              |
| genre   | string  | yes      | e.g. `"Sci-Fi/Drama"`                    |
| rating  | number  | no       | e.g. IMDb-style rating out of 10         |
| creator | string  | no       | director (movie) or showrunner (tv)      |

## Endpoints

### `GET /titles`
Returns the full list of titles.

**Sample request**
```bash
curl http://127.0.0.1:5000/titles
```

**Sample response** — `200 OK`
```json
[
  {
    "id": 1,
    "title": "The Shape of Water",
    "year": 2017,
    "type": "movie",
    "genre": "Fantasy/Drama",
    "rating": 7.3,
    "creator": "Guillermo del Toro"
  },
  {
    "id": 9,
    "title": "Breaking Bad",
    "year": 2008,
    "type": "tv",
    "genre": "Crime/Drama",
    "rating": 9.5,
    "creator": "Vince Gilligan"
  }
]
```

### `GET /titles/:id`
Returns a single title by id.

**Sample request**
```bash
curl http://127.0.0.1:5000/titles/1
```

**Sample response** — `200 OK`
```json
{
  "id": 1,
  "title": "The Shape of Water",
  "year": 2017,
  "type": "movie",
  "genre": "Fantasy/Drama",
  "rating": 7.3,
  "creator": "Guillermo del Toro"
}
```

**Not found** — `404 Not Found`
```json
{ "error": "Title with id 999 not found." }
```

### `POST /titles`
Creates a new title. Required fields: `title`, `year`, `type`, `genre`.

**Sample request**
```bash
curl -X POST http://127.0.0.1:5000/titles \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Dune: Part Two",
        "year": 2024,
        "type": "movie",
        "genre": "Sci-Fi/Adventure",
        "rating": 8.5,
        "creator": "Denis Villeneuve"
      }'
```

**Sample response** — `201 Created`
```json
{
  "id": 18,
  "title": "Dune: Part Two",
  "year": 2024,
  "type": "movie",
  "genre": "Sci-Fi/Adventure",
  "rating": 8.5,
  "creator": "Denis Villeneuve"
}
```

**Missing required field** — `400 Bad Request`
```bash
curl -X POST http://127.0.0.1:5000/titles \
  -H "Content-Type: application/json" \
  -d '{"title": "Missing Year"}'
```
```json
{ "error": "Missing required field(s): year, type, genre" }
```

### `PUT /titles/:id`
Updates an existing title. Any subset of fields can be sent; only the fields
included in the body are changed.

**Sample request**
```bash
curl -X PUT http://127.0.0.1:5000/titles/1 \
  -H "Content-Type: application/json" \
  -d '{"rating": 7.5}'
```

**Sample response** — `200 OK`
```json
{
  "id": 1,
  "title": "The Shape of Water",
  "year": 2017,
  "type": "movie",
  "genre": "Fantasy/Drama",
  "rating": 7.5,
  "creator": "Guillermo del Toro"
}
```

**Not found** — `404 Not Found`
```json
{ "error": "Title with id 999 not found." }
```

### `DELETE /titles/:id`
Deletes a title by id.

**Sample request**
```bash
curl -X DELETE http://127.0.0.1:5000/titles/2
```

**Sample response** — `200 OK`
```json
{ "message": "Title with id 2 deleted." }
```

**Not found** — `404 Not Found`
```json
{ "error": "Title with id 999 not found." }
```

## Status Codes Used

| Code | Meaning                                              |
|------|-------------------------------------------------------|
| 200  | Successful GET, PUT, or DELETE                        |
| 201  | Successful POST (resource created)                    |
| 400  | Bad request — missing/invalid required field          |
| 404  | Resource not found                                    |

## Project Structure

```
movie-tv-api/
├── app.py            # Flask app, routes, validation, SQLite setup
├── requirements.txt  # Python dependencies
├── README.md
├── .gitignore
└── movies.db          # created automatically on first run (not committed)
```

## Live Deployment (optional bonus)

If deployed, the live base URL is: `<add your Render/Railway URL here>`

Example against the live link:
```bash
curl <your-live-url>/titles
```