from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers import router
from app.infrastructure.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Clean up resources if needed
    pass

app = FastAPI(
    title="Time Deposit Kata API",
    description="This is assignment for ikigai digital by Aviral Kaintura",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, tags=["Time Deposits"])