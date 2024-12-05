import os
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from pydantic import BaseModel

# Import database setup from appointment_db
from appointment_db import Appointment, SessionLocal

app = FastAPI()


@app.api_route("/", methods=["GET", "HEAD"])
async def read_root():
    return {"message": "Welcome to the Appointment Management System"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request and response
class AppointmentCreate(BaseModel):
    patient_name: str
    dentist_name: str
    appointment_date: datetime


class AppointmentResponse(BaseModel):
    id: int
    patient_name: str
    dentist_name: str
    appointment_date: datetime
    is_canceled: bool

    class Config:
        from_attributes = True

# Endpoint to create an appointment
@app.post("/appointments/", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    # Check for double-booking
    existing_appointment = (
        db.query(Appointment)
        .filter(
            Appointment.dentist_name == appointment.dentist_name,
            Appointment.appointment_date == appointment.appointment_date,
        )
        .first()
    )
    if existing_appointment:
        raise HTTPException(status_code=400, detail="Time slot already booked!")

    new_appointment = Appointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

# Endpoint to list appointments
@app.get("/appointments/", response_model=List[AppointmentResponse])
def list_appointments(date: datetime = None, dentist_name: str = None, db: Session = Depends(get_db)):
    query = db.query(Appointment)
    if date:
        query = query.filter(Appointment.appointment_date == date)
    if dentist_name:
        query = query.filter(Appointment.dentist_name == dentist_name)
    return query.all()

# Endpoint to cancel an appointment
@app.delete("/appointments/{appointment_id}", response_model=AppointmentResponse)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.is_canceled = True
    db.commit()
    db.refresh(appointment)
    return appointment


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("appointment_api:app", host="0.0.0.0", port=port)
