# doctor_patient_backend

A RESTful backend application built using FastAPI for managing doctors, patients, authentication, authorization, and doctor-patient assignments.

# Project Overview

The Doctor Patient Management API is a backend system that provides APIs to manage doctors and patients securely.
The application uses JWT authentication and role-based authorization to control access to protected endpoints.

# Tech Stack
1. Python 3.9+
2. FastAPI
3. Pydantic
4. SQLAlchemy 
5. SQLite 
6. JWT-based Authentication
7. Uvicorn

# Main Features
1. User registration and login
2.JWT authentication
3. Password hashing
4. Role-based authorization
5. Admin and Doctor roles
6. Doctor CRUD operations
7. Patient CRUD operations
8. Doctor-patient assignment
9. Input validation
10. Pagination
11. Doctor specialization filtering
12. Soft delete for doctors
13. SQLite database
14. Swagger API documentation

# Project Structure
doctor_patient_backend<br>
│<br>
├── app<br>
│   ├── __init__.py<br>
│   │<br>
│   ├── auth<br>
│   │   ├── security.py<br>
│   │   └── dependencies.py<br>
│   │   
│   │<br>
│   ├── models<br>
│   │   ├── __init__.py<br>
│   │   ├── user.py<br>
│   │   ├── doctor.py<br>
│   │   ├── patient.py<br>
│   │   └── doctor_patient.py<br>
│   │<br>
│   ├── schemas<br>
│   │   ├── auth.py<br>
│   │   ├── doctor.py<br>
│   │   ├── patient.py<br>
│   │   └── assignment.py<br>
│   │<br>
│   ├── routers<br>
│   │   ├── auth.py/<br>
│   │   ├── doctors.py/<br>
│   │   ├── patients.py/<br>
│   │   └── assignment.py/<br>
│   │<br>
│   ├── config.py<br>
│   ├── database.py<br>
│   └── main.py<br>
│<br>
├── .env<br>
├── .gitignore<br>
├── requirements.txt<br>
├── README.md<br>
└── doctor_patient.db<br>   

