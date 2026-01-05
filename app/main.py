from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, incidents, volunteers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeTracker API")


app.include_router(incidents.router)
app.include_router(volunteers.router)

@app.get("/")
def root():
    return {"message": "Welcome to SafeTracker API"}
