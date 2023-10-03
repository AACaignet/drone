from dataBase.dataBase import Base, SessionLocal, engine

from modules.drone import models

Base.metadata.create_all(bind=engine)

session = SessionLocal()
models.Base.metadata.create_all(bind=engine)

medications = [
    {
        "name": "Aspirina",
        "weight": 20,
        "code": "1",
    },
    {
        "name": "Duralgina",
        "weight": 20,
        "code": "3",
    },
    {
        "name": "Nasolan",
        "weight": 10,
        "code": "3",
    }
]

#Insert Medications
for medication in medications:
    db_record = models.Medication(**medication)
    session.add(db_record)
    session.commit()

# Insert a Drone
drone = models.Drone(
    serial = "1",
    model = "v5",
    weight = 90,
    battery = 100,
    state = "IDLE"
)
session.add(drone)
session.commit()
session.close()

