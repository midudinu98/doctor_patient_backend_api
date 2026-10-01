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

#  Installation

## 1. Create the Project
### Open a terminal and move to the project directory:
 **cd doctor_patient_backend**

## 2. Create Virtual Environment
** python -m venv venv
 Activate on Windows
 venv\Scripts\activate**

## 3. Install Dependencies
**pip install -r requirements.txt**

### If requirements.txt does not exist, install the packages manually:
** pip install fastapi uvicorn sqlalchemy pydantic-settings python-dotenv python-jose[cryptography] passlib[bcrypt] email-validator**
 
# Environment Variables

## Create a .env file in the project root.
**DATABASE_URL=sqlite:///./doctor_patient.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30**

Important
Do not commit the .env file to GitHub.
Add the following to .gitignore:
1. venv/
2. __pycache__/
3. *.pyc
4. .env
5. *.db
6. .pytest_cache/
7. .vscode/
8. .idea/

#Run the Application

##Start the FastAPI server:
**uvicorn app.main:app --reload**

##The application will run at:
**http://127.0.0.1:8000**

# API Documentation

##  FastAPI provides automatic interactive documentation.
**Swagger UI
http://127.0.0.1:8000/docs**

## FastAPI provides automatic interactive documentation.
**Swagger UI
http://127.0.0.1:8000/docs**

