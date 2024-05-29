from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL, Text
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    direccion = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    departamento = Column(String(100), nullable=False)
    codigo_postal = Column(String(10), nullable=False)
    pais = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=False)
    documento = Column(String(10), unique=True, nullable=False)
    email = Column(String(254), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)

    informacion_financiera = relationship("InformacionFinanciera", uselist=False, back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(nombre={self.nombre}, apellido={self.apellido})>"

class InformacionFinanciera(Base):
    __tablename__ = 'informacionfinanciera'

    id = Column(Integer, primary_key=True, index=True)
    ingresos = Column(DECIMAL(10, 2), nullable=False)
    egresos = Column(DECIMAL(10, 2), nullable=False)
    activos = Column(DECIMAL(10, 2), nullable=False)
    pasivos = Column(DECIMAL(10, 2), nullable=False)
    historial_crediticio = Column(Text, nullable=True)
    puntuacion_crediticia = Column(Integer, nullable=True)
    antiguedad_laboral = Column(Integer, nullable=False)
    tipo_empleo = Column(String(100), nullable=False)
    estado_civil = Column(String(50), nullable=False)
    numero_dependientes = Column(Integer, default=0, nullable=False)
    historial_bancario = Column(Text, nullable=True)
    garantias = Column(Text, nullable=True)
    tipo_vivienda = Column(String(100), nullable=False)
    educacion = Column(String(100), nullable=False)
    #documento = Column(String(10), nullable=False)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=True)

    cliente = relationship("Cliente", back_populates="informacion_financiera")

    def __repr__(self):
        return f"<InformacionFinanciera(ingresos={self.ingresos})>"
