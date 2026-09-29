Movies & TV Shows API + Frontend

A full-stack Movies & TV Shows application built for ITCC 14. The project contains a Flask REST API backend, SQLite database, and a plain HTML/CSS/JavaScript frontend.

Niche: Movies and TV Shows

Backend: Flask (Python) + SQLite

Frontend: HTML + CSS + JavaScript

Frontend communication: JavaScript Fetch API

CORS: Flask-CORS

Data: Movies and TV shows with title, year, type, genre, rating, and creator

Features
API

List all movies and TV shows

View a single title by ID

Create a new title

Edit an existing title

Delete a title

Validate required fields

Return appropriate HTTP status codes

Store data in SQLite

Frontend

The frontend provides a user interface for all API operations:

View all titles

View individual title details

Add a new movie or TV show

Edit an existing title

Delete a title

Display validation errors

Handle 404 errors

Display loading states

Communicate with the Flask API using the Fetch API

Nostalgic old-theatre inspired design

Project Structure
movie-show-api/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── movies.db
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── venv/

Backend Setup
Requirements

Python 3

Git

A web browser

1. Clone the repository
git clone <your-repo-url>
cd movie-show-api

2. Create a virtual environment

On Windows:

py -m venv venv
venv\Scripts\activate


On Mac/Linux:

python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt


The project uses Flask and Gunicorn. Flask-CORS is also required for browser access to the API.

If Flask-CORS is not installed, run:

pip install flask-cors

4. Run the server
python app.py


The server starts at:

http://127.0.0.1:5000


Keep this terminal window running while using the frontend.

You can test the API by opening:

http://127.0.0.1:5000/


or:

http://127.0.0.1:5000/titles


The database is created and seeded automatically when the application is first run.

Frontend Setup

The frontend is located inside the frontend folder.

frontend/
├── index.html
├── style.css
└── app.js

Running the frontend

With the Flask backend running, open:

frontend/index.html


in a web browser.

On Windows, you can open the folder with:

explorer C:\Users\XU\movie-show-api\frontend


Then double-click index.html.

The frontend connects to:

http://127.0.0.1:5000


Make sure the Flask server is running before using the frontend.

CORS

The backend enables CORS using Flask-CORS so that the browser frontend can communicate with the Flask API.

The Flask application includes:

from flask_cors import CORS


and:

app = Flask(__name__)
CORS(app)


This allows the frontend to make requests to the API from the browser.

Data Model
Field	Type	Required	Notes
id	integer	auto	Assigned by the server
title	string	yes	Name of the movie/show
year	integer	yes	Release year
type	string	yes	Must be movie or tv
genre	string	yes	Example: Sci-Fi/Drama
rating	number	no	Rating out of 10
creator	string	no	Director or showrunner
API Endpoints
GET /titles

Returns the full list of titles.

Example:

curl http://127.0.0.1:5000/titles


Response:

[
  {
    "id": 1,
    "title": "Friends",
    "year": 1994,
    "type": "tv",
    "genre": "Comedy/Romance",
    "rating": 8.9,
    "creator": "David Crane"
  }
]

GET /titles/:id

Returns a single title by ID.

Example:

curl http://127.0.0.1:5000/titles/1


Response:

{
  "id": 1,
  "title": "Friends",
  "year": 1994,
  "type": "tv",
  "genre": "Comedy/Romance",
  "rating": 8.9,
  "creator": "David Crane"
}

Not found

If the ID does not exist:

{
  "error": "Title with id 999 not found."
}


The API returns:

404 Not Found

POST /titles

Creates a new title.

Required fields:

title

year

type

genre

Example:

curl -X POST http://127.0.0.1:5000/titles ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Dune: Part Two\",\"year\":2024,\"type\":\"movie\",\"genre\":\"Sci-Fi/Adventure\",\"rating\":8.5,\"creator\":\"Denis Villeneuve\"}"


Response:

{
  "id": 21,
  "title": "Dune: Part Two",
  "year": 2024,
  "type": "movie",
  "genre": "Sci-Fi/Adventure",
  "rating": 8.5,
  "creator": "Denis Villeneuve"
}


Status:

201 Created

Validation error

If required fields are missing, the API returns:

400 Bad Request


Example:

{
  "error": "Missing required field(s): year, type, genre"
}


The frontend displays this validation message to the user.

PUT /titles/:id

Updates an existing title.

Example:

curl -X PUT http://127.0.0.1:5000/titles/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"rating\":7.5}"


Only the supplied fields are changed.

DELETE /titles/:id

Deletes a title.

Example:

curl -X DELETE http://127.0.0.1:5000/titles/2


Response:

{
  "message": "Title with id 2 deleted."
}

Status Codes
Code	Meaning
200	Successful GET, PUT, or DELETE
201	Successful POST
400	Bad request or validation error
404	Resource not found
Frontend and Fetch API

The frontend communicates with the backend using JavaScript's Fetch API.

For example, the list of titles is retrieved with:

const response = await fetch("http://127.0.0.1:5000/titles");
const titles = await response.json();


The frontend also uses Fetch API requests for:

GET     /titles
GET     /titles/:id
POST    /titles
PUT     /titles/:id
DELETE  /titles/:id


This allows the user to perform all API operations through the graphical interface instead of using curl or Postman.

Error and Loading States

The frontend handles several API states:

Loading while titles are being retrieved

Empty library when no titles exist

Validation errors from the API

404 errors when a title cannot be found

Connection errors when the Flask server is not running

Success messages after adding, editing, or deleting a title

Design

The frontend uses a nostalgic old movie theatre visual theme inspired by classic cinema.

The interface uses theatrical colors, typography, borders, and styling while keeping the application usable without requiring movie poster images.

Running the Complete Application
1. Start the backend

Open Command Prompt:

cd C:\Users\XU\movie-show-api


Activate the virtual environment:

venv\Scripts\activate


Start Flask:

python app.py


Leave this terminal running.

2. Open the frontend

Open another Command Prompt or File Explorer and navigate to:

C:\Users\XU\movie-show-api\frontend


Open:

index.html


in your browser.

3. Use the application

The frontend allows you to:

View all movies and TV shows

View details for an individual title

Add a new title

Edit a title

Delete a title

Trigger and view validation errors

Technologies Used

Python

Flask

Flask-CORS

SQLite

HTML

CSS

JavaScript

Fetch API

Git

GitHub

ITCC 14

This project was created as part of the ITCC 14 API Server and Frontend Lab.

The frontend extends the original REST API by providing a graphical interface for all CRUD operations.