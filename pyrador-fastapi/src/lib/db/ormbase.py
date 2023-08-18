from __future__ import annotations

from typing import Any, Dict, List, Optional, Type
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import Query
from sqlalchemy import Column, String, MetaData, Table
from uuid import uuid4

from .session import Session, session, engine
from .exception import DatabaseException

from src.lib.logging import getLogger

logger = getLogger(__name__)

OrmType = Type["OrmBase"]

def generate_id() -> str:
    return str(uuid4())

class OrmMeta:
    
    @declared_attr
    def __tablename__(cls):
        return f"t_{cls.__name__.lower()}"
    
    @declared_attr
    def id(cls):
        return Column('id', String, primary_key=True, index=True, default=generate_id)
    
    
    def save(self, db: Session = session()) -> 'OrmType':
        logger.debug(f"{type(self)}: saving #{self.id}")
        if not self.id or not type(self).get(db=db, id=self.id):
            logger.debug(f"{type(self)}: creating #{self.id}")
            db.add(self)
        db.commit()
        db.refresh(self)
        return self
        
    @property
    def meta_table(self) -> Table:
        return Table(self.__tablename__, metadata=MetaData(), autoload=True, autoload_with=engine)
    
    @property
    def columns(self) -> List[str]:
        return [c.name for c in self.meta_table.columns]
    
    def update(self, query: Dict[str, Any], db: Session = session()) -> None:
        columns = self.columns
        for key in query:
            if key not in columns:
                raise DatabaseException(f"{type(self)}: has no column {key}")
            logger.debug(f"{type(self)}: updating {key} to {query[key]} on #{self.id}")
            self.__setattr__(key, query[key])
        else:
            self.save(db)
    
    def delete(self, db: Session = session()) -> None:
        logger.debug(f"{type(self)}: deleting #{self.id}")
        try:
            db.delete(self)
            db.flush()
        except Exception as e:
            raise DatabaseException(e)
    
    
    @classmethod
    def _query(cls, db: Session = session()) -> Query:
        logger.debug(f"{cls.__name__}: generating database query")
        return db.query(cls)
    
    @classmethod
    def all(cls, db: Session = session()) -> List['OrmType']:
        logger.debug(f"{cls.__name__}: fetching all")
        return cls._query(db = db).all()
    
    @classmethod
    def get(cls, id: str, db: Session = session()) -> Optional['OrmType']:
        logger.debug(f"{cls.__name__}: fetching #{id}")
        return cls._query(db = db).get(id)
    
    
    @classmethod
    def _filter(cls, criterion: dict, db: Session = session()) -> Query:
        logger.debug(f"{cls.__name__}: filtering results using {' and '.join([f'{k}={criterion[k]}' for k in criterion])}")
        return cls._query(db = db).filter_by(**criterion)
    
    @classmethod
    def find_all(cls, criterion: dict, db: Session = session()) -> List['OrmType']:
        logger.debug(f"{cls.__name__}: fetching all with filter")
        return cls._filter(db = db, criterion = criterion).all()
    
    @classmethod
    def find_first(cls, criterion: dict, db: Session = session()) -> List['OrmType']:
        logger.debug(f"{cls.__name__}: fetching first with filter")
        return cls._filter(db = db, criterion = criterion).first()
    
    @classmethod
    def find_one(cls, criterion: dict, db: Session = session) -> Optional['OrmType']:
        logger.info(f"{cls.__name__}: fetching one with filter")
        matches = cls.find_all(db = db, criterion = criterion)
        
        if len(matches) == 0:
            logger.debug(f"{cls.__name__}: no match found")
            return None
        if len(matches) > 1:
            logger.warning(f"{cls.__name__}: too many matches found")
            return None
        
        return matches[0]
    
    
OrmBase = declarative_base(cls=OrmMeta)