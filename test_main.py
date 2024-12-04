import pytest
from fastapi.testclient import TestClient
from appointment_api import app
from appointment_db import SessionLocal, Appointment, Base, engine

client = TestClient(app)

# Setup and teardown the database for each test run
@pytest.fixture(scope="function")
def setup_db():
    # Create the tables before each test
    Base.metadata.create_all(bind=engine)
    
    # Cleanup (delete all appointments) before each test
    db = SessionLocal()
    db.query(Appointment).delete()
    db.commit()
    
    yield db  # Give the test access to the db
    
    # Cleanup after test run
    db.query(Appointment).delete()
    db.commit()
    db.close()


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Appointment Management System"}


def test_create_appointment(setup_db):
    response = client.post(
        "/appointments/",
        json={
            "patient_name": "John Doe",
            "dentist_name": "Dr. Smith",
            "appointment_date": "2024-12-06T10:00:00"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["patient_name"] == "John Doe"
    assert data["dentist_name"] == "Dr. Smith"
    assert data["is_canceled"] is False


def test_list_appointments(setup_db):
    # Create an appointment before testing the listing
    client.post(
        "/appointments/",
        json={
            "patient_name": "Alice Doe",
            "dentist_name": "Dr. Smith",
            "appointment_date": "2024-12-07T10:00:00"
        },
    )
    
    response = client.get("/appointments/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_cancel_appointment(setup_db):
    # Create an appointment to be canceled
    response = client.post(
        "/appointments/",
        json={
            "patient_name": "Alice Doe",
            "dentist_name": "Dr. Smith",
            "appointment_date": "2024-12-07T10:00:00"
        },
    )
    appointment_id = response.json()["id"]
    
    # Now cancel the appointment
    response = client.delete(f"/appointments/{appointment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["is_canceled"] is True
