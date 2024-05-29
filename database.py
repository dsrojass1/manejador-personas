from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL_DATABASE = 'postgresql://banco_user:isis2503@10.128.0.2:5432/banco_db'

URL_DATABASE = 'postgresql://usuario:pepe@localhost:5432/basealpes2'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()