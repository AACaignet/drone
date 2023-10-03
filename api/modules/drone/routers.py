from datetime import datetime
from sqlite3 import IntegrityError
from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ...dataBase.dataBase import get_db
from . import schemas,crud,models



router = APIRouter()


@router.get("/medications/", response_model=List[schemas.MedicationInDBBase])
def get_medications(search: str = None, skip: int=0, limit: int=100, db: Session=Depends(get_db)):

    if search:
        return db.query(models.Medication).filter(models.Medication.name.like(f'{search}%')).\
                        offset(skip).limit(limit).all()
        
    return db.query(models.Medication).offset(skip).limit(limit).all()

@router.post("/medications/", response_model=schemas.MedicationInDBBase)
async def create_medication(
    
    medication:schemas.MedicationCreate,
    file: UploadFile = File(...),
    db: Session=Depends(get_db)
    ):
    
    extention = file.filename.split('.')
    ext = extention[len(extention) -1]
    if ext not in ['jpg,png']:
        raise HTTPException(status_code=400, detail="The file must be a image with extension .jpg or .png")
    try:
        medication_created = await crud.create_medication(db,medication,file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.__dict__['orig'].pgerror)
    return medication_created


@router.get("/drones/", response_model=List[schemas.DroneInDBBase])
def get_drones(search: str = None, skip: int=0, limit: int=100, db: Session=Depends(get_db)):

    if search:
        return db.query(models.Drone).filter(models.Drone.serial.like(f'{search}%')).offset(skip).limit(limit).all()
        
    return db.query(models.Drone).offset(skip).limit(limit).all()

@router.get("/drones/availables", response_model=List[schemas.DroneInDBBase])
def get_drones_availables(skip: int=0, limit: int=100, db: Session=Depends(get_db)):

    return db.query(models.Drone).filter(models.Drone.state == 'IDLE', models.Drone.battery > 25).\
                                        offset(skip).limit(limit).all()

@router.get("/drones/delivery_availables", response_model=List[schemas.DroneInDBBase])
def get_drones_delivery_availables(skip: int=0, limit: int=100, db: Session=Depends(get_db)):

    return db.query(models.Drone).filter(models.Drone.state == 'LOADED').\
                                        offset(skip).limit(limit).all()
        

@router.get("/drones/{serial_number}/state/", response_model=schemas.DroneInDBBase)
def get_drones_state(serial_number: str, db: Session=Depends(get_db)):
        
    return db.query(models.Drone).filter(models.Drone.serial == serial_number).first()

@router.get("/drones/{serial_number}/loaded_medications/", response_model=schemas.DeliveryState)
def get_drones_loaded_medications(serial_number: str, db: Session=Depends(get_db)):

    drone = db.query(models.Drone).filter(models.Drone.serial == serial_number).first()
    loaded_delivery = db.query(models.Delivery).filter(models.Delivery.drone_id == drone.id,
                                                        models.Delivery.state == 'LOADED').first()   
    return loaded_delivery
    
@router.post("/drones/", response_model=schemas.DroneInDBBase)
def create_drone(
    drone:schemas.DroneCreate,
    db: Session=Depends(get_db)
    ):
    
    try:
        country_created = crud.create_drone(db,drone)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.__dict__['orig'].pgerror)
    return country_created


@router.post("/drones/load", response_model=schemas.DeliveryMedication)
def load_drone(
    load:schemas.LoadDrone,
    db: Session=Depends(get_db)
    ):
    
    drone = db.query(models.Drone).filter(models.Drone.serial == load.serial_number).first()

    if drone.state != "LOADED" or drone.battery <= 25:
        raise HTTPException(status_code=400, detail="Drone with serial number: {} not LOADED.".format(drone.serial))
    
    if drone.battery <= 25:
        raise HTTPException(status_code=400, detail="Drone with low battery.")

    correct_weight = crud.ckeck_loaded_medication(db,drone,load)
    
    if not correct_weight:
        raise HTTPException(status_code=400, detail='Weight grate than drone weight({})'.format(drone.weight))
    try:
        drone_loaded = crud.load_drone(db, drone, load)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.__dict__['orig'].pgerror)
    return drone_loaded

@router.post("/drones/{serial}/delivery", response_model=schemas.DeliveryState)
def delivery(
    serial:str,
    db: Session=Depends(get_db)
    ):

    try:
        drone = db.query(models.Drone).filter(models.Drone.serial == serial).first()
        drone.state = 'DELIVERING'
        drone.last_update_state = datetime.now()
        db.commit()


    except Exception as e:
        raise HTTPException(status_code=400, detail=e.__dict__['orig'].pgerror)
    return delivery

# # @router.put("/countries/", response_model=schemas.CountryInDB)
# # def update_country(country:schemas.country.CountryUpdate, db: Session=Depends(get_db), user = Depends(get_current_user)):
    
# #     #validated  = cruds.country.validate_attr(db,country,id)
# #     country_db = cruds.country.get(db,country.id)
# #     if not country_db:
# #          raise HTTPException(status_code=400, detail="Country not already registered.")
# #     try:
# #         contry_updated = cruds.country.update(db, country_db, country)
# #     except Exception as e:
# #         raise HTTPException(status_code=400, detail=e.__dict__['orig'].pgerror.split('DETAIL: ')[1])
    
# #     return contry_updated

# # @router.get("/countries/{id}", response_model = schemas.country.CountryInDB)
# # def get_country(id: int, db: Session=Depends(get_db), user = Depends(get_current_user)):
    
# #     country = cruds.country.filter_get(db.query(models.Country),'id', id).first()
# #     return country

# # @router.get("/countries/{id}/delete", response_model = schemas.country.CountryInDB)
# # def delete_country(id: int, db: Session=Depends(get_db), user = Depends(get_current_user)):
    
#     try:
#         country = cruds.country.remove(db, id)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="This Country can't be removed. Other objects depends of it.")
#     return country
#-------------------- End Country -------------------------#


