from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates"),
)

router = APIRouter(
    prefix="/app",
    tags=["Фронтенд"],
)


def render(request: Request, template_name: str, title: str):
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context={
            "title": title,
        },
    )


@router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return render(request, "notes/index.html", "Мои заметки")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return render(request, "auth/login.html", "Вход")


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return render(request, "auth/register.html", "Регистрация")


@router.get("/notes", response_class=HTMLResponse)
async def notes_page(request: Request):
    return render(request, "notes/index.html", "Мои заметки")


@router.get("/folders", response_class=HTMLResponse)
async def folders_page(request: Request):
    return render(request, "folders/index.html", "Папки")