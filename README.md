This project implements a microservices-based system for managing electronic invoices (ESF) with authentication and a mock tax service. It consists of three microservices built using FastAPI, PostgreSQL, Tortoise ORM, and Docker Compose.

## Table of Contents
- [Overview](#overview)
- [Microservices](#microservices)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview
The project is designed to handle electronic invoices (ESF) with a focus on modularity and scalability. It includes three microservices:
1. **Auth Service**: Handles user registration, login, and JWT-based authentication.
2. **ESF Service**: Provides CRUD operations for electronic invoices and communicates with the tax service.
3. **GNS Proxy**: A mock service simulating the behavior of a tax authority (GNS) for testing purposes.

## Microservices
### 1. Auth Service
- **Purpose**: Manages user authentication and authorization.
- **Features**:
  - User registration and login.
  - JWT token generation and validation.
  - Secure password hashing.
- **Endpoints**:
  - `POST /register`: Create a new user.
  - `POST /login`: Authenticate a user and receive a JWT token.
  - `GET /users/me`: Retrieve current user details (requires JWT).

### 2. ESF Service
- **Purpose**: Manages electronic invoices (ESF) and their submission to the tax service.
- **Features**:
  - Create, read, update, and delete ESF records.
  - Send ESF data to the GNS (via GNS Proxy for testing).
- **Endpoints**:
  - `POST /esf`: Create a new ESF.
  - `GET /esf/{id}`: Retrieve an ESF by ID.
  - `PUT /esf/{id}`: Update an existing ESF.
  - `DELETE /esf/{id}`: Delete an ESF.
  - `POST /esf/submit`: Submit an ESF to the GNS.

### 3. GNS Proxy
- **Purpose**: A mock service simulating the tax authority (GNS) for testing.
- **Features**:
  - Accepts ESF submissions and returns predefined responses.
  - Simulates success, failure, or delay scenarios for testing resilience.
- **Endpoints**:
  - `POST /gns/submit`: Mock endpoint for ESF submission.

## Tech Stack
- **FastAPI**: High-performance, asynchronous web framework for building APIs.
- **Tortoise ORM**: Asynchronous ORM for managing PostgreSQL database interactions.
- **PostgreSQL**: Relational database for storing user and ESF data.
- **Docker Compose**: Containerization for easy deployment and development.
- **Python 3.11+**: Programming language for all services.

## Prerequisites
Before running the project, ensure you have the following installed:
- [Docker](https://www.docker.com/get-started) (with Docker Compose)
- [Git](https://git-scm.com/downloads)
- (Optional) Python 3.11+ and Poetry for local development without Docker.

## Installation and Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sheazer/FastAPI_gns.git
   cd FastAPI_gns
   ```

2. **Set up environment variables**:
   - Create a `.env` file in the project root based on the provided `.env.example`:
     ```bash
     cp .env.example .env
     ```
   - Update `.env` with your configuration (e.g., database credentials, JWT secret):
     ```env
     # Database
     POSTGRES_USER=admin
     POSTGRES_PASSWORD=secret
     POSTGRES_DB=fastapi_gns
     POSTGRES_HOST=db
     POSTGRES_PORT=5432

     # JWT
     JWT_SECRET=your_jwt_secret_key
     JWT_ALGORITHM=HS256
     JWT_EXPIRE_MINUTES=30
     ```

3. **(Optional) Local Python setup without Docker**:
   - Install [Poetry](https://python-poetry.org/docs/#installation).
   - Install dependencies:
     ```bash
     poetry install
     ```
   - Ensure a local PostgreSQL instance is running and matches the `.env` configuration.

## Running the Project
1. **Using Docker Compose** (recommended):
   - Build and start all services:
     ```bash
     docker-compose up --build
     ```
   - This will start:
     - Auth Service (`http://localhost:8001`)
     - ESF Service (`http://localhost:8002`)
     - GNS Proxy (`http://localhost:8003`)
     - PostgreSQL database

2. **Stop the services**:
   ```bash
   docker-compose down
   ```

3. **Running locally without Docker**:
   - Navigate to each service folder (`auth_service`, `esf_service`, `gns_proxy`) and run:
     ```bash
     poetry run uvicorn main:app --host 0.0.0.0 --port <port>
     ```
     Replace `<port>` with `8001` for Auth, `8002` for ESF, and `8003` for GNS Proxy.

## API Documentation
Each service provides interactive API documentation via Swagger:
- Auth Service: `http://localhost:8001/docs`
- ESF Service: `http://localhost:8002/docs`
- GNS Proxy: `http://localhost:8003/docs`

Example API usage with `curl`:
```bash
# Register a user
curl -X POST "http://localhost:8001/register" -H "Content-Type: application/json" -d '{"username": "user", "password": "pass123"}'

# Login and get JWT
curl -X POST "http://localhost:8001/login" -H "Content-Type: application/json" -d '{"username": "user", "password": "pass123"}'

# Create an ESF (use JWT from login response)
curl -X POST "http://localhost:8002/esf" -H "Authorization: Bearer <your_jwt_token>" -H "Content-Type: application/json" -d '{"title": "Invoice 001", "amount": 100.50}'
```

## Project Structure
```
FastAPI_gns/
├── auth_service/        # Authentication service
│   ├── main.py         # FastAPI app for auth
│   ├── models/         # Tortoise ORM models
│   └── routes/         # API endpoints
├── esf_service/        # ESF management service
│   ├── main.py
│   ├── models/
│   └── routes/
├── gns_proxy/         # Mock GNS service
│   ├── main.py
│   └── routes/
├── docker-compose.yml  # Docker Compose configuration
├── .env.example       # Example environment variables
└── README.md          # Project documentation
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please ensure your code follows:
- PEP 8 style guidelines (use `flake8` or `black`).
- Includes tests (use `pytest` and `pytest-asyncio`).
- Updates documentation if needed.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
