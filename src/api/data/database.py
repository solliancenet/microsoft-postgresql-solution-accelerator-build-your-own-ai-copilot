from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import KeyVaultConfigProvider

config_provider = KeyVaultConfigProvider()

postgresql_connection_string = config_provider.get_postgresql_connection_string()

engine = create_engine(postgresql_connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()