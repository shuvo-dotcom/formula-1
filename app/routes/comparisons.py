from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.firestore import get_collection
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/comparisons", tags=["comparisons"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/drivers", response_class=HTMLResponse)
async def compare_drivers(request: Request, driver1: str, driver2: str):
    drivers_ref = get_collection("drivers")
    d1 = drivers_ref.document(driver1).get().to_dict()
    d2 = drivers_ref.document(driver2).get().to_dict()
    return templates.TemplateResponse("comparisons/driver_comparison.html", {
        "request": request, "driver1": d1, "driver2": d2
    })
