from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .modules.drone import crud, models, routers, schemas
from .dataBase.dataBase import Base, SessionLocal, engine
#from dataBase.dataBase import get_db

# Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(routers.router)
