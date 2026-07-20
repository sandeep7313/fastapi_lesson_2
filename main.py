from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
import schemas

# Create database tables in Neon DB
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Retrieve Upstash Redis URL from environment
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        try:
            # Connect to Redis using asyncio Redis client
            redis = aioredis.from_url(redis_url, encoding="utf8", decode_responses=True)
            FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
            print("Successfully initialized Upstash Redis cache backend")
        except Exception as e:
            print(f"Failed to initialize Redis cache backend: {e}")
    else:
        print("WARNING: REDIS_URL not set. Endpoint caching will not be enabled.")
    
    yield

app = FastAPI(title="FastAPI Neon & Upstash Redis Cache API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "FastAPI with Neon DB and Upstash Redis Cache is running!", "docs_url": "/docs"}

@app.post("/items/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=list[schemas.ItemResponse])
@cache(expire=60)
def get_items(db: Session = Depends(get_db)):
    # This print statement will only show up when the cache misses (goes to DB)
    print("Database query executed: Fetching all items from database")
    items = db.query(models.Item).all()
    return items

@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
@cache(expire=60)
def get_item(item_id: int, db: Session = Depends(get_db)):
    # This print statement will only show up when the cache misses (goes to DB)
    print(f"Database query executed: Fetching item {item_id} from database")
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
