from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine, import_all_entities
from app.modules.profile.controller.ProfileController import router as profile_router
from app.modules.trip.controller.TripController import router as trip_router
from app.modules.task.controller.TaskController import router as task_router
from app.modules.sos.controller.SosController import router as sos_router
from app.modules.card.controller.CardController import router as card_router
from app.modules.guide.controller.GuideController import router as guide_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    import_all_entities()
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

app.include_router(profile_router)
app.include_router(trip_router)
app.include_router(task_router)
app.include_router(sos_router)
app.include_router(card_router)
app.include_router(guide_router)
