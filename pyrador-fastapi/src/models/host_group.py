from pydantic import BaseModel, Field
from typing import List

from host import HostBaseSchema


class HostGroupBaseSchema(BaseModel):
    
    name: str
    
    class Config:
        orm_mode = True


class HostGroupSchema(HostGroupBaseSchema):
    
    hosts: List[HostBaseSchema] = Field(default_factory=list)