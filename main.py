from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Base, Auto, get_db, engine
from schemas import AutoCreate, AutoResponse
from sqlalchemy import create_engine

# Crea todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Endpoint para crear un nuevo auto
@app.post("/autos/", response_model=AutoResponse)
def create_auto(auto: AutoCreate, db: Session = Depends(get_db)):
    new_auto = Auto(nombre=auto.nombre, precio=auto.precio, fechaFabricacion=auto.fechaFabricacion, activo=auto.activo)
    db.add(new_auto)
    db.commit()
    db.refresh(new_auto)
    return new_auto

# Endpoint para obtener una lista de todos los autos
@app.get("/autos/", response_model=list[AutoResponse])
def read_autos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    autos = db.query(Auto).offset(skip).limit(limit).all()
    return autos

# Endpoint para obtener un auto por ID
@app.get("/autos/{auto_id}", response_model=AutoResponse)
def read_auto(auto_id: int, db: Session = Depends(get_db)):
    auto = db.query(Auto).filter(Auto.id == auto_id).first()
    if auto is None:
        raise HTTPException(status_code=404, detail="Auto not found")
    return auto

# Endpoint para actualizar un auto por ID
@app.put("/autos/{auto_id}", response_model=AutoResponse)
def update_auto(auto_id: int, auto: AutoCreate, db: Session = Depends(get_db)):
    db_auto = db.query(Auto).filter(Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Auto not found")
    db_auto.nombre = auto.nombre
    db_auto.precio = auto.precio
    db_auto.fechaFabricacion = auto.fechaFabricacion
    db_auto.activo = auto.activo
    db.commit()
    db.refresh(db_auto)
    return db_auto

# Endpoint para eliminar un auto por ID
@app.delete("/autos/{auto_id}", response_model=AutoResponse)
def delete_auto(auto_id: int, db: Session = Depends(get_db)):
    db_auto = db.query(Auto).filter(Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Auto not found")
    db.delete(db_auto)
    db.commit()
    return db_auto
