from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.firestore import get_collection
from fastapi.templating import Jinja2Templates
from app.models.team import Team

router = APIRouter(prefix="/teams", tags=["teams"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_teams(request: Request):
    teams_ref = get_collection("teams").stream()
    teams = [team.to_dict() for team in teams_ref]
    return templates.TemplateResponse("teams/list.html", {"request": request, "teams": teams})

@router.post("/add")
async def add_team(team: Team):
    teams_ref = get_collection("teams")
    teams_ref.document(team.name).set(team.dict())
    return {"status": "Team added successfully"}
