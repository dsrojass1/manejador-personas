from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

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
    fecha_nacimiento: str

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int

    class Config:
        orm_mode: True

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
    documento: str = Field(..., max_length=10)
    cliente_id: Optional[int] = None

class InformacionFinancieraCreate(InformacionFinancieraBase):
    pass

class InformacionFinanciera(InformacionFinancieraBase):
    id: int

    class Config:
        orm_mode: True