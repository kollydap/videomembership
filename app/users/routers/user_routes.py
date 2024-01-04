from fastapi import APIRouter, status, Body, Depends, Request, Form
from fastapi.responses import HTMLResponse
import app.users.utils as user_utils
from pydantic import ValidationError
from app.users.models import UserSignupSchema, UserLoginSchema

# from app.core.application import TEMPLATE_DIR
import pathlib, json

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
def user_login_get_view(request: Request):
    return templates.TemplateResponse(
        name="/auth/login.html", context={"request": request}
    )


@api_router.post(path="/login", response_class=HTMLResponse)
def login_post_view(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    raw_Data = {
        "email": email,
        "password": password,
    }
    data, errors = user_utils.valid_schema_data_or_error(
        raw_data=raw_Data, SchemaModel=UserLoginSchema
    )
    return templates.TemplateResponse(
        name="/auth/login.html",
        context={"request": request, "data": data, "errors": errors},
    )


@api_router.get(path="/signup", response_class=HTMLResponse)
def user_signup_get_view(request: Request):
    return templates.TemplateResponse(
        name="/auth/signup.html", context={"request": request}
    )


@api_router.post(path="/signup", response_class=HTMLResponse)
def signup_post_view(
    # if it waas Api we could set the model here
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
):
    raw_Data = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm,
    }
    data, errors = user_utils.valid_schema_data_or_error(
        raw_data=raw_Data, SchemaModel=UserSignupSchema
    )
    return templates.TemplateResponse(
        name="/auth/signup.html",
        context={"request": request, "data": data, "errors": errors},
    )
