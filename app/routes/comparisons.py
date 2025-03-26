from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.firestore import fetch_two_documents, fetch_all_documents

router = APIRouter(prefix="/comparisons", tags=["comparisons"])
templates = Jinja2Templates(directory="app/templates")

# Compare drivers form page
@router.get("/drivers", response_class=HTMLResponse)
async def compare_drivers_form(request: Request):
    drivers = fetch_all_documents("drivers")
    return templates.TemplateResponse("comparisons/drivers.html", {
        "request": request,
        "drivers": drivers
    })

# Display drivers comparison results
@router.post("/drivers/results", response_class=HTMLResponse)
async def compare_drivers_results(
    request: Request,
    driver1: str = Form(...),
    driver2: str = Form(...)
):
    driver_data1, driver_data2 = fetch_two_documents("drivers", driver1, driver2)
    return templates.TemplateResponse("comparisons/driver_results.html", {
        "request": request,
        "driver1": driver_data1,
        "driver2": driver_data2
    })

# Compare teams form page
@router.get("/teams", response_class=HTMLResponse)
async def compare_teams_form(request: Request):
    teams = fetch_all_documents("teams")
    return templates.TemplateResponse("comparisons/teams.html", {
        "request": request,
        "teams": teams
    })

# Display teams comparison results
@router.post("/teams/results", response_class=HTMLResponse)
async def compare_teams_results(
    request: Request,
    team1: str = Form(...),
    team2: str = Form(...)
):
    team_data1, team_data2 = fetch_two_documents("teams", team1, team2)
    return templates.TemplateResponse("comparisons/team_results.html", {
        "request": request,
        "team1": team_data1,
        "team2": team_data2
    })
