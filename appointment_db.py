from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Appointment model
class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    dentist_name = Column(String, nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    is_canceled = Column(Boolean, default=False)

# Database setup
DATABASE_URL = "postgresql://root:P@$$w@rd18@localhost:5432/appointments_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
