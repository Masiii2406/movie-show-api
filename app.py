from flask import Flask, request, jsonify, g
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movies.db")

app = Flask(__name__)

REQUIRED_FIELDS = ["title", "year", "type", "genre"]


def get_db():
    """Open a new database connection if there isn't one for this request."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the table (if needed) and seed it with hand-crafted data."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            type TEXT NOT NULL,
            genre TEXT NOT NULL,
            rating REAL,
            creator TEXT
        )
        """
    )
    count = conn.execute("SELECT COUNT(*) FROM titles").fetchone()[0]
    if count == 0:
        seed = [
            ("Friends", 1994, "tv", "Comedy/Romance", 8.9, "David Crane"),
            ("Modern Family", 2009, "tv", "Comedy", 8.4, "Christopher Lloyd"),
            ("How I Met Your Mother", 2005, "tv", "Comedy/Romance", 8.3, "Carter Bays"),
            ("Meet Joe Black", 1998, "movie", "Romance/Fantasy", 7.1, "Martin Brest"),
            ("Demolition", 2015, "movie", "Drama", 7.0, "Jean-Marc Vallee"),
            ("The Secret Life of Walter Mitty", 2013, "movie", "Adventure/Comedy", 7.3, "Ben Stiller"),
            ("Good Will Hunting", 1997, "movie", "Drama", 8.3, "Gus Van Sant"),
            ("The Shape of Water", 2017, "movie", "Fantasy/Drama", 7.3, "Guillermo del Toro"),
            ("Parasite", 2019, "movie", "Thriller/Drama", 8.5, "Bong Joon-ho"),
            ("Spirited Away", 2001, "movie", "Animation/Fantasy", 8.6, "Hayao Miyazaki"),
            ("The Grand Budapest Hotel", 2014, "movie", "Comedy/Drama", 8.1, "Wes Anderson"),
            ("Mad Max: Fury Road", 2015, "movie", "Action/Adventure", 8.1, "George Miller"),
            ("Whiplash", 2014, "movie", "Drama/Music", 8.5, "Damien Chazelle"),
            ("Breaking Bad", 2008, "tv", "Crime/Drama", 9.5, "Vince Gilligan"),
            ("The Wire", 2002, "tv", "Crime/Drama", 9.3, "David Simon"),
            ("Fleabag", 2016, "tv", "Comedy/Drama", 8.7, "Phoebe Waller-Bridge"),
            ("Chernobyl", 2019, "tv", "Drama/History", 9.4, "Craig Mazin"),
            ("The Bear", 2022, "tv", "Comedy/Drama", 8.6, "Christopher Storer"),
            ("Severance", 2022, "tv", "Sci-Fi/Thriller", 8.7, "Dan Erickson"),
            ("Avatar: The Last Airbender", 2005, "tv", "Animation/Adventure", 9.3, "Michael Dante DiMartino"),
        ]
        conn.executemany(
            "INSERT INTO titles (title, year, type, genre, rating, creator) VALUES (?, ?, ?, ?, ?, ?)",
            seed,
        )
        conn.commit()
    conn.close()


def row_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "year": row["year"],
        "type": row["type"],
        "genre": row["genre"],
        "rating": row["rating"],
        "creator": row["creator"],
    }


def validate_payload(data, partial=False):
    """Return an error message string if invalid, else None.
    When partial=True (used for PUT on an existing resource), only
    validate the fields that are present rather than requiring all of them.
    """
    if not data or not isinstance(data, dict):
        return "Request body must be a JSON object."

    fields_to_check = REQUIRED_FIELDS if not partial else [f for f in REQUIRED_FIELDS if f in data]

    if not partial:
        missing = [f for f in REQUIRED_FIELDS if f not in data or data[f] in (None, "")]
        if missing:
            return f"Missing required field(s): {', '.join(missing)}"

    if "year" in data and data["year"] not in (None, ""):
        try:
            int(data["year"])
        except (ValueError, TypeError):
            return "Field 'year' must be an integer."

    if "type" in data and data["type"] not in (None, ""):
        if data["type"] not in ("movie", "tv"):
            return "Field 'type' must be either 'movie' or 'tv'."

    return None


@app.route("/titles", methods=["GET"])
def get_titles():
    db = get_db()
    rows = db.execute("SELECT * FROM titles").fetchall()
    return jsonify([row_to_dict(r) for r in rows]), 200


@app.route("/titles/<int:title_id>", methods=["GET"])
def get_title(title_id):
    db = get_db()
    row = db.execute("SELECT * FROM titles WHERE id = ?", (title_id,)).fetchone()
    if row is None:
        return jsonify({"error": f"Title with id {title_id} not found."}), 404
    return jsonify(row_to_dict(row)), 200


@app.route("/titles", methods=["POST"])
def create_title():
    data = request.get_json(silent=True)
    error = validate_payload(data, partial=False)
    if error:
        return jsonify({"error": error}), 400

    db = get_db()
    cur = db.execute(
        "INSERT INTO titles (title, year, type, genre, rating, creator) VALUES (?, ?, ?, ?, ?, ?)",
        (
            data["title"],
            int(data["year"]),
            data["type"],
            data["genre"],
            data.get("rating"),
            data.get("creator"),
        ),
    )
    db.commit()
    new_row = db.execute("SELECT * FROM titles WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(new_row)), 201


@app.route("/titles/<int:title_id>", methods=["PUT"])
def update_title(title_id):
    db = get_db()
    existing = db.execute("SELECT * FROM titles WHERE id = ?", (title_id,)).fetchone()
    if existing is None:
        return jsonify({"error": f"Title with id {title_id} not found."}), 404

    data = request.get_json(silent=True)
    error = validate_payload(data, partial=True)
    if error:
        return jsonify({"error": error}), 400

    updated = {
        "title": data.get("title", existing["title"]),
        "year": int(data["year"]) if "year" in data and data["year"] not in (None, "") else existing["year"],
        "type": data.get("type", existing["type"]),
        "genre": data.get("genre", existing["genre"]),
        "rating": data.get("rating", existing["rating"]),
        "creator": data.get("creator", existing["creator"]),
    }

    db.execute(
        "UPDATE titles SET title = ?, year = ?, type = ?, genre = ?, rating = ?, creator = ? WHERE id = ?",
        (
            updated["title"],
            updated["year"],
            updated["type"],
            updated["genre"],
            updated["rating"],
            updated["creator"],
            title_id,
        ),
    )
    db.commit()
    row = db.execute("SELECT * FROM titles WHERE id = ?", (title_id,)).fetchone()
    return jsonify(row_to_dict(row)), 200


@app.route("/titles/<int:title_id>", methods=["DELETE"])
def delete_title(title_id):
    db = get_db()
    existing = db.execute("SELECT * FROM titles WHERE id = ?", (title_id,)).fetchone()
    if existing is None:
        return jsonify({"error": f"Title with id {title_id} not found."}), 404

    db.execute("DELETE FROM titles WHERE id = ?", (title_id,))
    db.commit()
    return jsonify({"message": f"Title with id {title_id} deleted."}), 200


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Movies & TV Shows API is running.",
        "endpoints": {
            "GET /titles": "list all titles",
            "GET /titles/<id>": "get a single title",
            "POST /titles": "create a title",
            "PUT /titles/<id>": "update a title",
            "DELETE /titles/<id>": "delete a title",
        },
    }), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
