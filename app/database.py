from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=1800,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def import_all_entities():
    from app.modules.profile.entity.ProfileEntity import ProfileEntity
    from app.modules.trip.entity.TripEntity import TripEntity
    from app.modules.task.entity.TaskEntity import TaskEntity
    from app.modules.sos.entity.SosRecordEntity import SosRecordEntity
    from app.modules.card.entity.MemoryCardEntity import MemoryCardEntity
