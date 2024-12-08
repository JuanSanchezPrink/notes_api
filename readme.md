# Notes API

This is a simple Notes API built with Flask, which allows users to create, read, update, and delete notes. The API also integrates Swagger for documentation.

## Features

- **Create**: Add new notes with a title and content.
- **Read**: Retrieve a list of all notes or a specific note by its ID.
- **Update**: Modify the title and content of an existing note.
- **Delete**: Remove a note by its ID.

## Setup

To set up and run the project locally, follow these steps:

### 1. Clone the repository

Run the following command to clone the repository:

`git clone https://github.com/JuanSanchezPrink/notes`

Change into the project directory:

`cd notes-api`

### 2. Create a virtual environment

For Windows:

`python -m venv venv`

For macOS/Linux:

`python3 -m venv venv`

### 3. Activate the virtual environment

For Windows:

`venv\Scripts\activate`

### 4. Install dependencies

Run the following command to install the required dependencies:

`pip install -r requirements.txt`

### 5. Run the application

Use the following command to start the Flask app:

`python app.py`

The application will run locally on `http://127.0.0.1:5000`.

### 6. Swagger Documentation

The API has integrated Swagger documentation. Once the application is running, open the following URL to view the documentation:

`http://127.0.0.1:5000/apidocs/`

## Endpoints

### `GET api/notes`
Retrieve all notes with paginated.

**Response:**
- Status: `200 OK`
- Body: A list of all notes in JSON format.

### `GET api/notes/<note_id>`
Retrieve a single note by its ID.

**Parameters:**
- `note_id`: The ID of the note.

**Response:**
- Status: `200 OK` if the note is found.
- Status: `404 Not Found` if the note does not exist.

### `POST api/notes`
Create a new note.

**Body:**

{
  "title": "Note Title",
  "content": "Content of the note"
}

**Response:**
- Status: `201 Created`
- Body: The created note.

### `PUT api/notes/<note_id>`
Update an existing note by its ID.

**Parameters:**
- `note_id`: The ID of the note to update.

**Body:**

{
  "title": "Updated Title",
  "content": "Updated content"
}

**Response:**
- Status: `200 OK` if the note is updated successfully.
- Status: `404 Not Found` if the note does not exist.
- Status: `400 Bad Request` if the body is missing required fields.

### `DELETE api/notes/<note_id>`
Delete a note by its ID.

**Parameters:**
- `note_id`: The ID of the note to delete.

**Response:**
- Status: `200 OK` if the note is deleted successfully.
- Status: `404 Not Found` if the note does not exist.

## Running Tests

To run the tests, use the following command:

`python -m unittest tests/test_notes.py`

Make sure the virtual environment is activated before running the tests.

## Author

- **Juan Sanchez** - [GitHub Profile](https://github.com/JuanSanchezPrink)
