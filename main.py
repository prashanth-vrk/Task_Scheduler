from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from task_manager import add_task, get_tasks
from ws_manager import ws_manager

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return templates.TemplateResponse("dashboard.html", {"request": {}})

@app.post("/submit_task")
async def submit_task(execution_time: int):
    task_id = add_task(execution_time)
    return {"task_id": task_id}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    while True:
        tasks = get_tasks()
        await ws_manager.broadcast(str(tasks))
