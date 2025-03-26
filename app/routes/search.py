from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.firestore import search_documents

router = APIRouter(prefix="/search", tags=["search"])
templates = Jinja2Templates(directory="app/templates")

# Search Drivers - form page
@router.get("/drivers", response_class=HTMLResponse)
async def search_drivers_form(request: Request):
    return templates.TemplateResponse("search/drivers.html", {"request": request})

# Handle Drivers search results
@router.post("/drivers/results", response_class=HTMLResponse)
async def search_drivers_results(
    request: Request,
    field: str = Form(...),
    comparison: str = Form(...),
    value: str = Form(...)
):
    results = search_documents("drivers", field, comparison, parse_value(value))
    return templates.TemplateResponse("search/driver_results.html", {
        "request": request,
        "drivers": results
    })

# Search Teams - form page
@router.get("/teams", response_class=HTMLResponse)
async def search_teams_form(request: Request):
    return templates.TemplateResponse("search/teams.html", {"request": request})

# Handle Teams search results
@router.post("/teams/results", response_class=HTMLResponse)
async def search_teams_results(
    request: Request,
    field: str = Form(...),
    comparison: str = Form(...),
    value: str = Form(...)
):
    results = search_documents("teams", field, comparison, parse_value(value))
    return templates.TemplateResponse("search/team_results.html", {
        "request": request,
        "teams": results
    })

# Helper function to parse numerical values correctly
def parse_value(value):
    try:
        return int(value)
    except ValueError:
        return value
