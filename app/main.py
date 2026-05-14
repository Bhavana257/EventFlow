# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import orders, products
from app.models.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup — engine is already verified connected by database.py
    Base.metadata.create_all(bind=engine)
    print(" Tables created / verified.")
    yield
    # Runs on shutdown (add cleanup here later if needed)


app = FastAPI(lifespan=lifespan)

app.include_router(orders.router, prefix="/api", tags=["Orders"])
app.include_router(products.router, prefix="/api", tags=["Products"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {"message": "Welcome to EventFlow 🚀"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
