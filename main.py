
# Import FastAPI class for creating the app
from fastapi import FastAPI
# Import the auth and tasks routers from the routers package
from routers import auth, tasks

# Create a FastAPI app instance with a custom title
app = FastAPI(title="Task-Manager App")

# Register the auth router with the app
app.include_router(auth.router)
# Register the tasks router with the app
app.include_router(tasks.router)

# Define the root endpoint ("/") of the API
@app.get("/")
def read_root():
    # Return a welcome message as a JSON response
    return {"message": "Welcome to the Task-Manager App!"}

