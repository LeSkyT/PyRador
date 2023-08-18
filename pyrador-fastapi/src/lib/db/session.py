from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.lib.configuration import Settings

settings = Settings().database


engine = create_engine(settings.dsn)

sessionFactory = sessionmaker(
    autoflush=settings.auto_flush,
    autocommit=settings.auto_commit,
    bind=engine
)

# Dependency
@property
def session() -> Session:
    return sessionFactory()