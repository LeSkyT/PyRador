from pydantic import BaseModel, Field
from typing import List
from sqlalchemy import Column, String

from src.lib.db import OrmBase

from .host_group import HostGroupBaseSchema


class Host(OrmBase):
    hostname: Column(String, unique=True, primary_key=True)


class HostBaseSchema(BaseModel):
    
    hostname: str
    
    class Config:
        orm_mode = True


class HostSchema(HostBaseSchema):
    
    groups: List[HostGroupBaseSchema] = Field(default_factory=list)
