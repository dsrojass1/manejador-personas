from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener el objeto de sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# Endpoints

# Clientes
@app.post("/clientes/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.get("/clientes/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
    return clientes

@app.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@app.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    for key, value in cliente.dict().items():
        setattr(db_cliente, key, value)

    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.delete("/clientes/{cliente_id}", response_model=schemas.Cliente)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(db_cliente)
    db.commit()
    return db_cliente

# InformaciónFinanciera
@app.post("/informacion_financiera/", response_model=schemas.InformacionFinanciera)
def create_informacion_financiera(info: schemas.InformacionFinancieraCreate, db: Session = Depends(get_db)):
    db_info = models.InformacionFinanciera(**info.dict())
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info

@app.get("/informacion_financiera/", response_model=List[schemas.InformacionFinanciera])
def read_informacion_financiera(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    informacion = db.query(models.InformacionFinanciera).offset(skip).limit(limit).all()
    return informacion

@app.get("/informacion_financiera/{info_id}", response_model=schemas.InformacionFinanciera)
def read_informacion_financiera(info_id: int, db: Session = Depends(get_db)):
    db_info = db.query(models.InformacionFinanciera).filter(models.InformacionFinanciera.id == info_id).first()
    if db_info is None:
        raise HTTPException(status_code=404, detail="Información financiera no encontrada")
    return db_info

@app.put("/informacion_financiera/{info_id}", response_model=schemas.InformacionFinanciera)
def update_informacion_financiera(info_id: int, info: schemas.InformacionFinancieraCreate, db: Session = Depends(get_db)):
    db_info = db.query(models.InformacionFinanciera).filter(models.InformacionFinanciera.id == info_id).first()
    if db_info is None:
        raise HTTPException(status_code=404, detail="Información financiera no encontrada")
    
    for key, value in info.dict().items():
        setattr(db_info, key, value)

    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info

@app.delete("/informacion_financiera/{info_id}", response_model=schemas.InformacionFinanciera)
def delete_informacion_financiera(info_id: int, db: Session = Depends(get_db)):
    db_info = db.query(models.InformacionFinanciera).filter(models.InformacionFinanciera.id == info_id).first()
    if db_info is None:
        raise HTTPException(status_code=404, detail="Información financiera no encontrada")
    
    db.delete(db_info)
    db.commit()
    return db_info
