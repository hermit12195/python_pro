from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routers import user_routes, post_routes
from app.db.session import init_db
from app.websocket.endpoints import register_ws_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
app = FastAPI(title="Async FastAPI", lifespan=lifespan)
app.include_router(user_routes.router)
app.include_router(post_routes.router)
register_ws_routes(app)