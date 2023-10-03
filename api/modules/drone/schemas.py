from decimal import Decimal
import json
from pickletools import float8
from typing import List, Optional
from fastapi import File, UploadFile

from pydantic import BaseModel, Field, FilePath, validator

from ...modules.drone.types import StateEnumn


class DroneBase(BaseModel):

    serial:Optional[str] = Field(title="Serial Number",max_length=100)
    

    class Config:
        orm_mode = True

class Drone(DroneBase):

    model:Optional[str] = Field(title="Serial Number",max_length=100)
    weight:Optional[Decimal] = Field(title="Serial Number", lt=500,gte=1)
    state:Optional[StateEnumn] = Field(title="State")

class DroneCreate(Drone):
    pass

class DroneUpdate(Drone):
    id: int
    pass

class DroneInDBBase(Drone):
    id: int
    battery:float

    class Config:
        orm_mode = True

class MedicationBase(BaseModel):

    name:Optional[str] = Field(title="Name",max_length=100)
    code:Optional[str] = Field(title="Code",max_length=100)

    class Config:
        orm_mode = True

class Medication(MedicationBase):
    
    weight:Optional[float] = Field(title="Weight")
    image:Optional[str] = None

class MedicationCreate(BaseModel):
    
    name:Optional[str] = None
    code:Optional[str] = None
    weight:Optional[float] = None
    image:Optional[str] = None
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class MedicationInDBBase(Medication):
    id: Optional[int] = None


class LoadMedication(BaseModel):

    id:int
    weight:Optional[float] = Field(title="Weight")

class DeliveryBase(BaseModel):

    state:Optional[str] = Field(title="Name",max_length=100)
    large:Optional[float] = None

    class Config:
        orm_mode = True

class DeliveryMedication(BaseModel):

    medication: MedicationBase
    weight: float


    class Config:
        orm_mode = True

class DeliveryState(DeliveryBase):

    delivery_medications:List[DeliveryMedication]


    class Config:
        orm_mode = True

class LoadDrone(BaseModel):

    serial_number:str
    delivery_range:float
    medications:List[LoadMedication]
    

class DroneLoadedMedications(DroneBase):

    deliveries: List[DeliveryState]

    @validator('deliveries')
    def check_uniques_values(cls, v, **kwargs):

        return [item for item in v if item.state == 'LOADED']
        # if kwargs.get('field').name in ['country', 'country_en', 'country_es', 'country_fr', 'country_it']:
            
        #     return v
        # return v
    
    
# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []

#     class Config:
#         orm_mode = True