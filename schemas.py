from pydantic import BaseModel, EmailStr, Field, SecretStr
from typing import List, Optional
from datetime import date

class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    direccion: str
    ciudad: str
    departamento: str
    codigo_postal: str
    pais: str
    telefono: str
    documento: str = Field(..., max_length=10)
    email: EmailStr
    fecha_nacimiento: date

class ClienteCreate(ClienteBase):
    username: str
    password: SecretStr
    pass



class InformacionFinancieraBase(BaseModel):
    ingresos: float
    egresos: float
    activos: float
    pasivos: float
    historial_crediticio: Optional[str] = None
    puntuacion_crediticia: Optional[int] = None
    antiguedad_laboral: int
    tipo_empleo: str
    estado_civil: str
    numero_dependientes: int = 0
    historial_bancario: Optional[str] = None
    garantias: Optional[str] = None
    tipo_vivienda: str
    educacion: str
    #documento: str = Field(..., max_length=10)
    cliente_id: Optional[int] = None

class InformacionFinancieraCreate(InformacionFinancieraBase):
    pass

class InformacionFinanciera(InformacionFinancieraBase):
    id: int

    class Config:
        orm_mode: True

class Cliente(ClienteBase):
    id: int
    informacion_financiera: Optional[InformacionFinanciera] = None

    class Config:
        orm_mode: True