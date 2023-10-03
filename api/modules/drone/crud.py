import os
from fastapi import File
import aiofiles
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from ...settings import BASE_DIR
from . import models, schemas

# DRONE


def create_drone(db: Session, obj_in: schemas.DroneCreate):

        
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = models.Drone(**obj_in_data)  # type: ignore
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

async def save_image(file:File):

    async with aiofiles.open(os.path.join(BASE_DIR,'statics/images/') + file.filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

async def create_medication(db: Session, obj_in: schemas.DroneCreate,file:File):

        
    obj_in_data = jsonable_encoder(obj_in)
    obj_in_data.update({"image": file.filename})
    db_obj = models.Medication(**obj_in_data)  # type: ignore
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    await save_image(file)
    
    return db_obj

def update_drone_state(db: Session, db_obj:models.Drone,value):
    obj_data = jsonable_encoder(db_obj)
        
    setattr(db_obj, 'state', value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return obj_data

def ckeck_loaded_medication(db: Session, drone, load: schemas.LoadDrone):
    
    delivery_weight = 0
    for item in load.medications:
        delivery_weight += item.weight
    
    if delivery_weight <= drone.weight:
        return True

    return False

def load_drone(db: Session,drone, load: schemas.LoadDrone):

    drone_updated = update_drone_state(db,drone,'LOADING')
    
    delivery_obj = models.Delivery(drone_id = drone.id,large = load.delivery_range)
    
    db.add(delivery_obj)
    db.commit()
    db.refresh(delivery_obj)

    delivery_weight = 0
    for item in load.medications:

        delivery_weight += item.weight
        deliv_medic_obj = models.DeliveryMedication(delivery_id = delivery_obj.id,medication_id = item.id,weight = item.weight)
        db.add(deliv_medic_obj)
        db.commit()
        db.refresh(deliv_medic_obj)
    
    delivery_obj.weight = delivery_weight
    delivery_obj.state = 'LOADED'
    db.commit()
    db.refresh(delivery_obj)
    
    drone = update_drone_state(db,drone,'LOADED')

    return delivery_obj
