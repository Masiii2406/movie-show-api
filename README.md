# Movies & TV Shows API

A REST API server for a hand-crafted catalog of movies and TV shows, built for the
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
python -m venv venv
venv\Scripts\activate      # on Mac/Linux: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server (this also creates and seeds movies.db on first run)
python app.py
```

> Note: on Windows use `python`; on Mac/Linux use `python3` if `python` isn't mapped.

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
    "title": "Friends",
    "year": 1994,
    "type": "tv",
    "genre": "Comedy/Romance",
    "rating": 8.9,
    "creator": "David Crane"
  },
  {
    "id": 7,
    "title": "Good Will Hunting",
    "year": 1997,
    "type": "movie",
    "genre": "Drama",
    "rating": 8.3,
    "creator": "Gus Van Sant"
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
  "title": "Friends",
  "year": 1994,
  "type": "tv",
  "genre": "Comedy/Romance",
  "rating": 8.9,
  "creator": "David Crane"
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
  "id": 21,
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
  "title": "Friends",
  "year": 1994,
  "type": "tv",
  "genre": "Comedy/Romance",
  "rating": 9.0,
  "creator": "David Crane"
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

If deployed, the live base URL is: `<add your Render URL here after deploying>`

### Deploying to Render (free tier)

1. Push this repo to GitHub (already done if you're reading this on GitHub).
2. Go to [render.com](https://render.com) and sign up / log in (you can sign in with GitHub).
3. Click **New +** → **Web Service**.
4. Connect your GitHub account and select this repository.
5. Fill in:
   - **Name:** anything, e.g. `movie-tv-api`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
6. Click **Create Web Service**. Render will build and deploy — this takes a couple of minutes.
7. Once it's live, Render gives you a URL like `https://movie-tv-api-xxxx.onrender.com`.

Example against the live link:
```bash
curl https://<your-app-name>.onrender.com/titles
```

> Note: Render's free tier spins the service down after inactivity, so the first
> request after a while may take 30-60 seconds to respond while it wakes up.
