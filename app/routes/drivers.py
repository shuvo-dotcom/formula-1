from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.firestore import fetch_all_documents, fetch_document, get_collection
from app.models.driver import Driver

router = APIRouter(prefix="/drivers", tags=["drivers"])
templates = Jinja2Templates(directory="app/templates")

# List all drivers
@router.get("/", response_class=HTMLResponse)
async def drivers_list(request: Request):
    drivers = fetch_all_documents("drivers")
    return templates.TemplateResponse("drivers/list.html", {
        "request": request,
        "drivers": drivers
    })

# Show create driver form (specific route first)
@router.get("/create", response_class=HTMLResponse)
async def create_driver_form(request: Request):
    return templates.TemplateResponse("drivers/create.html", {"request": request})

# Handle create driver form submission
@router.post("/add")
async def add_driver(
    name: str = Form(...),
    age: int = Form(...),
    team: str = Form(...),
    pole_positions: int = Form(...),
    race_wins: int = Form(...),
    points_scored: int = Form(...),
    world_titles: int = Form(...),
    fastest_laps: int = Form(...)
):
    driver_data = Driver(
        name=name,
        age=age,
        team=team,
        pole_positions=pole_positions,
        race_wins=race_wins,
        points_scored=points_scored,
        world_titles=world_titles,
        fastest_laps=fastest_laps
    )
    driver_ref = get_collection("drivers").document(name)
    driver_ref.set(driver_data.dict())
    return RedirectResponse(url="/drivers/", status_code=303)

# Edit driver form (also specific, must be before generic)
@router.get("/edit/{driver_name}", response_class=HTMLResponse)
async def edit_driver_form(request: Request, driver_name: str):
    driver = fetch_document("drivers", driver_name)
    if not driver:
        return HTMLResponse("Driver not found", status_code=404)
    return templates.TemplateResponse("drivers/edit.html", {
        "request": request,
        "driver": driver
    })

# Handle edit driver form submission
@router.post("/edit/{driver_name}")
async def edit_driver(
    driver_name: str,
    age: int = Form(...),
    team: str = Form(...),
    pole_positions: int = Form(...),
    race_wins: int = Form(...),
    points_scored: int = Form(...),
    world_titles: int = Form(...),
    fastest_laps: int = Form(...)
):
    driver_data = {
        "name": driver_name,
        "age": age,
        "team": team,
        "pole_positions": pole_positions,
        "race_wins": race_wins,
        "points_scored": points_scored,
        "world_titles": world_titles,
        "fastest_laps": fastest_laps
    }
    driver_ref = get_collection("drivers").document(driver_name)
    driver_ref.update(driver_data)
    return RedirectResponse(url=f"/drivers/{driver_name}", status_code=303)

# Generic detail route LAST!
@router.get("/{driver_name}", response_class=HTMLResponse)
async def driver_detail(request: Request, driver_name: str):
    driver = fetch_document("drivers", driver_name)
    if not driver:
        return HTMLResponse("Driver not found", status_code=404)
    return templates.TemplateResponse("drivers/detail.html", {
        "request": request,
        "driver": driver
    })
