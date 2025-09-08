(# Task-Manager App

A FastAPI-based Task Manager application with Supabase backend for authentication and task storage.

## Features
- User registration and login (Supabase Auth)
- Create, read, update, and delete tasks
- Filter tasks by owner
- Pydantic models for validation and documentation
- RESTful API structure

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## Installation
1. Clone the repository:
	```sh
	git clone <your-repo-url>
	cd Task-Manager-app
	```
2. Install dependencies:
	```sh
	pip install -r requirements.txt
	```
3. Set up your `.env` file with your Supabase credentials:
	```env
	SUPABASE_URL=your_supabase_url
	SUPABASE_KEY=your_supabase_key
	```

## Running the App
Start the FastAPI server with Uvicorn:
```sh
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Auth
- `POST /auth/register` — Register a new user
- `POST /auth/login` — Login and get a token

### Tasks
- `POST /tasks` — Create a new task
- `GET /tasks` — List all tasks (optionally filter by owner_id)
- `GET /tasks/{task_id}` — Get a task by ID
- `PUT /tasks/{task_id}` — Update a task
- `DELETE /tasks/{task_id}` — Delete a task

## Testing
Run tests with:
```sh
pytest
```

## Project Structure

```
├── main.py            # FastAPI app entry point
├── database.py        # Supabase client setup
├── requirements.txt   # Python dependencies
├── routers/
│   ├── auth.py        # Auth endpoints
│   └── tasks.py       # Task endpoints
│   └── tests/         # Test files
└── README.md
```

## License
MIT
