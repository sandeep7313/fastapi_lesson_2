from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="FastAPI Lesson 2 API",
    description="FastAPI application deployed on Vercel",
    version="1.0.0"
)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get("/")
def read_root():
    return {
        "message": "Welcome to FastAPI Lesson 2!",
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "fastapi-lesson-2"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "query": q}

@app.post("/items")
def create_item(item: Item):
    return {"message": "Item created successfully", "item": item}
