from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.routers.cards import router as cards_router
from app.routers.guide import router as guide_router
from app.routers.profiles import router as profiles_router
from app.routers.sos import router as sos_router
from app.routers.tasks import router as tasks_router
from app.routers.trips import router as trips_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profiles_router)
app.include_router(trips_router)
app.include_router(sos_router)
app.include_router(tasks_router)
app.include_router(cards_router)
app.include_router(guide_router)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")
@app.get("/")
def root():
    return FileResponse(static_dir / "index.html")
