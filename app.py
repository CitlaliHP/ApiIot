from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
import os

app = FastAPI()

engine = create_engine('sqlite:///apiIot.db', connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Iot(Base):
    __tablename__ = "iot"

    id = Column(Integer, primary_key=True, index=True)
    dispositivo = Column(String(80))
    valor = Column(Integer)

Base.metadata.create_all(bind=engine)

class IotIn(BaseModel):
    dispositivo: str
    valor: int

@app.post("/iot")
def create_iot(iot_in: IotIn):
    db = SessionLocal()
    iot = Iot(**iot_in.dict())
    db.add(iot)
    db.commit()
    db.refresh(iot)
    return iot

@app.get("/{id}")
def get_device(id: int):
    db = SessionLocal()
    device = db.query(Iot).get(id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return {'id': device.id, 'dispositivo': device.dispositivo, 'valor': device.valor}

@app.patch("/{id}/{value}")
def update_device(id: int, value: int):
    db = SessionLocal()
    device = db.query(Iot).get(id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    device.valor = value
    db.commit()
    return {'valor': device.valor}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)