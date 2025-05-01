from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="app/templates")

def register_ws_routes(app):
    @app.get("/", response_class=HTMLResponse)
    def read_index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                data = await  websocket.receive_text()
                await websocket.send_text(f"The message text is: {data}")
        except WebSocketDisconnect:
            print("Client disconnected")
