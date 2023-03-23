from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Todo

# Methods to interact with MongoDB
from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)

# Instantiating Fast API
app = FastAPI()

# Path to React Front-end
origins = ["https://localhost:3000", "http://localhost:3000"]

# Adding middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Decorator to get the empty route
@app.get("/")
def read_root():
    return {"message": "Hello World"}


# Get all To Dos
@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response


# Get an specific To Do
@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_title(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"Not Todo item found with this title:  {title}")


# Create a new To Do
@app.post("/api/todo/", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong (bad request)")


# Update a to do
@app.put("/api/todo/{title}", response_model=Todo)
async def put_todo(title: str, description: str):
    response = await update_todo(title, description)
    if response:
        return response
    raise HTTPException(404, f"Not Todo item found with this title: {title}")


# Delete a to do
@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return f"Successfully deleted {title}"
    raise HTTPException(404, f"Not Todo item found with this title: {title}")
