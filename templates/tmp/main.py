from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles  # Импорт для работы со статикой
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

# Маршрут для статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/registration", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@app.get("/auth", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def read_catalog(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/edit-profile", response_class=HTMLResponse)
async def read_checkout(request: Request):
    return templates.TemplateResponse("edit-profile.html", {"request": request})

@app.get("/cart", response_class=HTMLResponse)
async def read_account(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})

@app.get("/product-card", response_class=HTMLResponse)
async def read_account(request: Request):
    return templates.TemplateResponse("product-card.html", {"request": request})

@app.get("/order", response_class=HTMLResponse)
async def read_account(request: Request):
    return templates.TemplateResponse("order-info.html", {"request": request, "user_name": "Иван Иванов"})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
