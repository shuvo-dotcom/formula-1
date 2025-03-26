from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.firestore import get_collection
from fastapi.templating import Jinja2Templates
from app.models.driver import Driver

router = APIRouter(prefix="/drivers", tags=["drivers"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_drivers(request: Request):
    drivers_ref = get_collection("drivers").stream()
    drivers = [driver.to_dict() for driver in drivers_ref]
    return templates.TemplateResponse("drivers/list.html", {"request": request, "drivers": drivers})

@router.post("/add")
async def add_driver(driver: Driver):
    drivers_ref = get_collection("drivers")
    drivers_ref.document(driver.name).set(driver.dict())
    return {"status": "Driver added successfully"}
