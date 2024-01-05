from app.core import config
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

settings = config.get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))
# BASE_DIR  = settings.base_dir


def render(
    request,
    template_name: str,
    context: dict,
    status_code: int = 200,
    cookies: dict = {},
):
    # we use copy so that changes made to ctx will not aaffect context
    ctx = context.copy()
    ctx.update({"request": request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str, status_code=status_code)
    if len(cookies.keys()) > 0:
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)
    for key in request.cookies.keys():
        response.delete_cookie(key=key)
    return response
