from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.firestore import get_collection, fetch_document, fetch_all_documents
from app.models.team import Team

router = APIRouter(prefix="/teams", tags=["teams"])
templates = Jinja2Templates(directory="app/templates")

# List all teams
@router.get("/", response_class=HTMLResponse)
async def list_teams(request: Request):
    teams = fetch_all_documents("teams")
    return templates.TemplateResponse("teams/list.html", {
        "request": request,
        "teams": teams
    })

# Show create team form (specific, placed first)
@router.get("/create", response_class=HTMLResponse)
async def create_team_form(request: Request):
    return templates.TemplateResponse("teams/create.html", {"request": request})

# Handle create team form submission
@router.post("/add")
async def add_team(
    name: str = Form(...),
    year_founded: int = Form(...),
    pole_positions: int = Form(...),
    race_wins: int = Form(...),
    constructor_titles: int = Form(...),
    previous_season_position: int = Form(...)
):
    team_data = Team(
        name=name,
        year_founded=year_founded,
        pole_positions=pole_positions,
        race_wins=race_wins,
        constructor_titles=constructor_titles,
        previous_season_position=previous_season_position
    )
    team_ref = get_collection("teams").document(name)
    team_ref.set(team_data.dict())
    return RedirectResponse(url="/teams/", status_code=303)

# Edit team form (specific, placed before generic)
@router.get("/edit/{team_name}", response_class=HTMLResponse)
async def edit_team_form(request: Request, team_name: str):
    team = fetch_document("teams", team_name)
    if not team:
        return HTMLResponse("Team not found", status_code=404)
    return templates.TemplateResponse("teams/edit.html", {
        "request": request,
        "team": team
    })

# Handle edit team form submission
@router.post("/edit/{team_name}")
async def edit_team(
    team_name: str,
    year_founded: int = Form(...),
    pole_positions: int = Form(...),
    race_wins: int = Form(...),
    constructor_titles: int = Form(...),
    previous_season_position: int = Form(...)
):
    team_data = {
        "name": team_name,
        "year_founded": year_founded,
        "pole_positions": pole_positions,
        "race_wins": race_wins,
        "constructor_titles": constructor_titles,
        "previous_season_position": previous_season_position
    }
    team_ref = get_collection("teams").document(team_name)
    team_ref.update(team_data)
    return RedirectResponse(url=f"/teams/{team_name}", status_code=303)

# Generic detail route (always last!)
@router.get("/{team_name}", response_class=HTMLResponse)
async def team_detail(request: Request, team_name: str):
    team = fetch_document("teams", team_name)
    if not team:
        return HTMLResponse("Team not found", status_code=404)
    return templates.TemplateResponse("teams/detail.html", {
        "request": request,
        "team": team
    })
