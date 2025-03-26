from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import auth, drivers, teams, comparisons

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(drivers.router)
app.include_router(teams.router)
app.include_router(comparisons.router)

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def root():
    return {"message": "Welcome to the Formula 1 Database App"}
