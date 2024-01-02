from fastapi import APIRouter, status, Body, Depends, Request, Form
from fastapi.responses import HTMLResponse

# from app.core.application import TEMPLATE_DIR
import pathlib

from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)

TEMPLATE_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

api_router = APIRouter()


@api_router.get(path="/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {"request": request.cookies}
    return templates.TemplateResponse(name="/users/home.html", context=context)


@api_router.get(path="/login", response_class=HTMLResponse)
def user_sgnup_get_view(request: Request):
    return templates.TemplateResponse(
        name="/auth/login.html", context={"request": request}
    )


# @api_router.post(path="/login", response_class=HTMLResponse)
# def login_post_view(
#     request: Request, email: str = Form(...), password: str = Form(...)
# ):
#     return templates.TemplateResponse(name="/auth/login.html")
