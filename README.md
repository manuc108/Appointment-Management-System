# Appointment Management System

The Appointment Management System is a RESTful API developed using FastAPI and SQLAlchemy that allows users to manage appointment scheduling. The system enables:

- Booking an appointment with patient and dentist details.
- Listing all appointments for a specific date or dentist.
- Canceling an appointment.

## Features

1. **Book Appointments**: Create a new appointment by specifying the patient name, dentist name, and appointment date.
2. **List Appointments**: Retrieve appointments filtered by date or dentist name.
3. **Cancel Appointments**: Mark an appointment as canceled.

---

## Installation and Setup

### Prerequisites

- Python 3.8+
- Virtual Environment (recommended)
- SQLite (default database)

### Clone the Repository

```bash
$ git clone https://github.com/manuc108/appointment-management-system.git
$ cd appointment-management-system
```

### Create and Activate a Virtual Environment

```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

Install the required Python packages:

```bash
$ pip install -r requirements.txt
```

### Database Setup

The application uses SQLite as the default database. The database file `appointments.db` will be automatically created in the project directory when you run the application for the first time.

---

## Running the Application

Start the FastAPI server using the following command:

```bash
$ uvicorn appointment_api:app --reload
```

By default, the server will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### Root Endpoint

- **GET /**
  - Response: `{ "message": "Welcome to the Appointment Management System" }`

### Create Appointment

- **POST /appointments/**
  - Request Body:
    ```json
    {
      "patient_name": "John Doe",
      "dentist_name": "Dr. Smith",
      "appointment_date": "2024-12-06T14:00:00"
    }
    ```
  - Response:
    ```json
    {
      "id": 1,
      "patient_name": "John Doe",
      "dentist_name": "Dr. Smith",
      "appointment_date": "2024-12-06T14:00:00",
      "is_canceled": false
    }
    ```

### List Appointments

- **GET /appointments/**
  - Query Parameters:
    - `date` (optional): Filter by appointment date (ISO format).
    - `dentist_name` (optional): Filter by dentist name.
  - Response:
    ```json
    [
      {
        "id": 1,
        "patient_name": "John Doe",
        "dentist_name": "Dr. Smith",
        "appointment_date": "2024-12-06T14:00:00",
        "is_canceled": false
      }
    ]
    ```

### Cancel Appointment

- **DELETE /appointments/{appointment_id}**
  - Path Parameter: `appointment_id` (integer)
  - Response:
    ```json
    {
      "id": 1,
      "patient_name": "John Doe",
      "dentist_name": "Dr. Smith",
      "appointment_date": "2024-12-06T14:00:00",
      "is_canceled": true
    }
    ```

---

## Project Structure

```plaintext
appointment-management-system/
|├── appointment_api.py    # Rest APIs
|├── appointment_db.py     # Database models and setup
|├── appointments.db       # SQLite database (generated at runtime)
|├── Procfile              # To deploy a service
|├── requirements.txt      # Python dependencies
|└── README.md             # Project documentation
|├── test_main.py          # FastAPI app and endpoints
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes.

---

## Contact

For questions or support, please contact:

- Email: (mailto:manu.v23csai@nst.rishihood.edu.in)
- GitHub: [Manu vahan](https://github.com/manuc108)

