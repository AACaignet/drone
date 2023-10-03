import os
import csv
from datetime import datetime,timedelta
from .celery_tasks import app
from ..dataBase.dataBase import SessionLocal
from ..modules.drone import models

@app.task
def check_battery():
    
    session = SessionLocal()
    drones = session.query(models.Drone).all()
    with open('drone_state_battery_log.tx','w') as f:
        f.writelines('Drone Serial Number  % Battery\n')
        for drone in drones:

            f.writelines('{}   {} \n'.format(drone.serial,drone.battery))

        f.close()
    session.close()

@app.task
def check_drone_state():
    
    time_now = datetime.now()
    session = SessionLocal()
    drones = session.query(models.Drone).filter(models.Drone.state != 'LOADED')
    with open('drone_state_log.tx','w') as f:
        f.writelines('Serial Number  % State\n')
        for drone in drones:

            last_update = drone.last_update_state
            if drone.state == "DELIVERING" and time_now - timedelta(hours=last_update.hour,minutes=last_update.minute)> 5 :
               drone.state = "DELIVERED"
               drone.last_update_state = datetime.now()
               session.add(drone) 
               session.commit()

            if drone.state == "DELIVERED" and time_now - timedelta(hours=last_update.hour,minutes=last_update.minute)> 5 :
               drone.state = "RETURNING"
               drone.last_update_state = datetime.now()
               session.add(drone) 
               session.commit()

            if drone.state == "RETURNING" and time_now - timedelta(hours=last_update.hour,minutes=last_update.minute)> 5 :
               drone.state = "IDLED"
               drone.last_update_state = datetime.now()
               session.add(drone) 
               session.commit() 

            f.writelines('{}   {} \n'.format(drone.serial,drone.state))
        
        f.close()
    session.close()
