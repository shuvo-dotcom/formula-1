from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes import auth, drivers, teams, comparisons, home, search, comparisons

app = FastAPI()

# Include your existing routers
app.include_router(auth.router)
app.include_router(drivers.router)
app.include_router(teams.router)
app.include_router(comparisons.router)
app.include_router(home.router)
app.include_router(search.router)
app.include_router(comparisons.router)

# Redirect root to login page
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/auth/login")
