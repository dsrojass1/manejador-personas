from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas
import requests
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import joinedload
from urlMicroservicios import PATH_AUTH


# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

ALGORITHM = "HS256"
SECRET_KEY = 'django-insecure-0%eqg^5(^sps_c31(j1lsm6ffnac2unepfv8^&2f5ycd0)p0u3'

http_bearer = HTTPBearer()

async def get_current_user(token: str = Depends(http_bearer)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception
    
# Dependencia para obtener el objeto de sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# Endpoints

# Clientes
def verificarPermisosUsuarios(usuarioBody, cliente_id):
    if usuarioBody["idPersona"] != cliente_id and usuarioBody["rol"] != "asesor":
        raise HTTPException(status_code=403, detail="No tiene permisos para ver este recurso")
    
def verificarPermisosASesor(usuarioBody):
    if usuarioBody["rol"] != "asesor":
        raise HTTPException(status_code=403, detail="No tiene permisos para ver este recurso")
    
@app.post("/clientes/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    username = cliente.username
    password = cliente.password.get_secret_value()
    db_cliente = models.Cliente(**cliente.dict(exclude={"username", "password"}))
    db.add(db_cliente)
    db.flush()
    cliente_id = db_cliente.id
    body = {"username": username, "password": password, "rol": "cliente", "idPersona": cliente_id, "email": cliente.email}
    peticionAutenticacion = requests.post(PATH_AUTH, json=body)
    if peticionAutenticacion.status_code != 201:
        print(peticionAutenticacion.json())
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al crear el usuario")
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.get("/clientes/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), usuarioBody: dict = Depends(get_current_user)):
    verificarPermisosASesor(usuarioBody)
    clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
    return clientes

# @app.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
# def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
#     db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
#     if db_cliente is None:
#         raise HTTPException(status_code=404, detail="Cliente no encontrado")
#     return db_cliente
@app.get("/clientes/{cliente_id}", response_model=schemas.Cliente, status_code= 200)  # Change the response model here
def read_cliente(cliente_id: int, db: Session = Depends(get_db), usuarioBody: dict = Depends(get_current_user)):
    # db_cliente = db.query(models.Cliente).options(joinedload(models.Cliente.informacion_financiera)).filter(models.Cliente.id == cliente_id).first()
    verificarPermisosUsuarios(usuarioBody, cliente_id)
    db_cliente = db.query(models.Cliente).options(joinedload(models.Cliente.informacion_financiera)).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente


@app.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db), usuarioBody: dict = Depends(get_current_user)):
    verificarPermisosUsuarios(usuarioBody, cliente_id)
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
def delete_cliente(cliente_id: int, db: Session = Depends(get_db), usuarioBody: dict = Depends(get_current_user)):
    verificarPermisosUsuarios(usuarioBody, cliente_id)
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()
    return db_cliente

# InformaciónFinanciera
@app.post("/informacion_financiera/", response_model=schemas.InformacionFinanciera)
def create_informacion_financiera(info: schemas.InformacionFinancieraCreate, db: Session = Depends(get_db), usuarioBody: dict = Depends(get_current_user)):
    verificarPermisosUsuarios(usuarioBody, info.cliente_id)
    print("sadfasd")
    cliente = db.query(models.Cliente).filter(models.Cliente.id == info.cliente_id).first()
    if cliente == None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
    db_info = models.InformacionFinanciera(**info.dict())
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info

@app.get("/informacion_financiera/", response_model=List[schemas.InformacionFinanciera])
def read_informacion_financiera(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), usuarioBody: dict = Depends(get_current_user)):
    verificarPermisosASesor(usuarioBody)
    informacion = db.query(models.InformacionFinanciera).offset(skip).limit(limit).all()
    print(informacion)
    return informacion

@app.get("/informacion_financiera/{cliente_id}", response_model=schemas.InformacionFinanciera)
def read_informacion_financiera(cliente_id: int, db: Session = Depends(get_db), usuarioBody: dict = Depends(get_current_user)):
    verificarPermisosUsuarios(usuarioBody, cliente_id)
    db_info = db.query(models.InformacionFinanciera).filter(models.InformacionFinanciera.cliente_id == cliente_id).first()
    if db_info is None:
        raise HTTPException(status_code=404, detail="Información financiera no encontrada")
    return db_info

@app.put("/informacion_financiera/{cliente_id}", response_model=schemas.InformacionFinanciera)
def update_informacion_financiera(cliente_id: int, info: schemas.InformacionFinancieraCreate, db: Session = Depends(get_db), usuarioBody: dict = Depends(get_current_user)):
    verificarPermisosUsuarios(usuarioBody, cliente_id)
    db_info = db.query(models.InformacionFinanciera).filter(models.InformacionFinanciera.cliente_id == cliente_id).first()
    if db_info is None:
        raise HTTPException(status_code=404, detail="Información financiera no encontrada")
    
    for key, value in info.dict().items():
        setattr(db_info, key, value)

    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info

@app.delete("/informacion_financiera/{cliente_id}", response_model=schemas.InformacionFinanciera)
def delete_informacion_financiera(cliente_id: int, db: Session = Depends(get_db), usuarioBody: dict = Depends(get_current_user)):
    verificarPermisosUsuarios(usuarioBody, cliente_id)
    db_info = db.query(models.InformacionFinanciera).filter(models.InformacionFinanciera.cliente_id == cliente_id).first()
    if db_info is None:
        raise HTTPException(status_code=404, detail="Información financiera no encontrada")
    
    db.delete(db_info)
    db.commit()
    return db_info
