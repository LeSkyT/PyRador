from src.lib.db import OrmBase, engine

from .host import Host, HostBaseSchema, HostSchema
from .host_group import HostGroup, HostGroupBaseSchema, HostGroupSchema


OrmBase.metadata.create_all(bind=engine)