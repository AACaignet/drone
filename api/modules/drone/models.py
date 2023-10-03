from datetime import datetime
from decimal import Decimal
from email.policy import default

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float,DateTime,UniqueConstraint
from sqlalchemy.orm import relationship

from ...dataBase.dataBase import Base


class Drone(Base):
    __tablename__ = 'drone'
    
    id = Column(Integer, primary_key=True, index=True)
    serial = Column(String(100),unique = True,nullable = False)
    model = Column(String(50),nullable = False)
    weight = Column(Float,nullable = False)
    battery = Column(Float,default = 100)
    state = Column(String(50),default = "LOADED")
    last_update_state = Column(DateTime,default = datetime.now())
    
    deliveries = relationship("Delivery", back_populates="drone")


class Medication(Base):
    __tablename__ = 'medication'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100),unique = True,nullable = False)
    weight = Column(Float,nullable = False)
    code = Column(String(100),nullable = False)
    image = Column(String(100),nullable = True)

    delivery_medications = relationship("DeliveryMedication", back_populates="medication")

class Delivery(Base):
    __tablename__ = 'delivery'
    
    id = Column(Integer, primary_key=True, index=True)
    drone_id = Column(Integer, ForeignKey("drone.id"))
    date_delivery = Column(DateTime,default = datetime.now())
    state = Column(String(50),default = "LOADING")
    large = Column(Float)
    weight = Column(Float,nullable = False,default = 0)
    
    delivery_medications = relationship("DeliveryMedication", back_populates="delivery")
    drone = relationship("Drone", back_populates="deliveries")

class DeliveryMedication(Base):
    __tablename__ = 'deliverymedication'
    
    id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("delivery.id"))
    medication_id = Column(Integer, ForeignKey("medication.id"))
    weight = Column(Float,nullable = False)

    delivery = relationship("Delivery", back_populates="delivery_medications")
    medication = relationship("Medication", back_populates="delivery_medications")
    
    __table_args__ = (UniqueConstraint('delivery_id', 'medication_id','weight', name='_deliv_med_weigth'),)
    
# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")