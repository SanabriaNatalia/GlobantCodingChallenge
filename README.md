# Globant Coding Challenge

## Project - Employee Management API

This project is part of the Globant coding challenge and involves creating an API to manage data related to employees, departments, and jobs. The API allows the insertion of new data, data exploration, and the creation of automated backups.

### Technologies used

- FastAPI: Python framework used to build the REST API.
- Docker: For containerization and deployment of the application.
- SQLAlchemy: ORM used to manage interactions with the PostgreSQL database.
- Azure:
    - Azure Database for PostgreSQL: SQL database hosted in the cloud.
    - Azure Container Registry: Container registry where the Docker image of the application is stored.
    - Azure Storage Data Lake Gen2: File system used to manage source XLSX files, create CSV files, and store backups.
    - Azure Container App: The application will be deployed here, running the Docker container in the cloud.

### Project structure:

```
GlobantCodingChallenge/
│
├── app/
│   ├── database/
│   │   ├── database_config.py  # Database configuration with SQLAlchemy
│   │   ├── database_models.py  # Data models (employees, departments, jobs)
│   │   ├── db_department.py    # ORM capabilities for the department entity
│   │   ├── db_hired_employee.py  # ORM capabilities for the hired_employee entity
│   │   ├── db_job.py           # ORM capabilities for the job entity
│   ├── routers/
│   │   ├── employees.py        # API routes related to employees
│   │   ├── departments.py      # API routes related to departments
│   │   ├── jobs.py             # API routes related to jobs
│   ├── schemas/                # Pydantic schemas for data validation
│   │   ├── department.py
│   │   ├── hired_employee.py
│   │   ├── job.py
│   ├── utils/
│   │   ├── save_csv.py         # code for saving xlsx files to csv
│   │   ├── load_csv.py         # code for loading csv to Azure PostgreSQL
├── ├── security /
│   │   ├── auth.py             # File that handles the authentication of the application
│   ├── main.py                 # FastAPI setup and main endpoint definitions
├── tests/
│   ├── test_api.py             # API tests
├── .env                        # Environment variables (not included in the repository for security)
├── Dockerfile                  # Instructions for building the Docker image
├── docker-compose.yml          # Service definitions for local deployment
├── .github/workflows/
│   ├── deploy.yml              # GitHub Actions for building and pushing the Docker image to Azure Container Registry
└── README.md                   # Project documentation
└── INSTRUCTIONS.md             # Instructions for the challenge
└── requirements.txt            # Libraries needed
└── requirements-dev.txt        # Extended libraries needed for testing and development

```

### Environment SetUp

1. **Clone the repository**

```
git clone https://github.com/your-username/GlobantCodingChallenge.git
cd GlobantCodingChallenge
```

2. **SetUp Environment Variables**

```
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@pg-globantchallenge-use-prod.postgres.database.azure.com:5432/${POSTGRES_DB}?sslmode=require
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=${ACCOUNT_NAME};AccountKey=${ACCOUNT_KEY};EndpointSuffix=core.windows.net
API_USERNAME=${USERNAME}
API_PASSWORD=${PASSWORD}
```

3. **Build and Run the Docker Image Locally:**

    Make sure to install Docker and have the daemon running.

```
docker-compose up --build
```

4. **Automatic Deployment with GitHub Actions:**

The project is configured with GitHub Actions to automatically build and push the Docker image to Azure Container Registry on every pull request to the main branch.

### Key Features

1. REST API

- Employee Management: Endpoints for creating, reading, and listing employees.
- Department and Job Management: Endpoints for managing departments and jobs, ensuring referential integrity.

2. Data Processing and Backup Handling:

- Azure Databricks is used to:
    - Run scripts for loading data from CSV files into the database.
    - Generate CSV files from XLSX files stored in Azure Storage Data Lake Gen2.
    - Create and manage data backups in AVRO format.
- Azure Storage Data Lake Gen2 serves as the file system to:
    - Store the source XLSX files.
    - Create and manage CSV files.
    - Store backups of the database.

3. Application Deployment

    The Dockerized application is deployed to Azure App Service, ensuring it is accessible and scalable in the cloud. 

### Technical Rationale

- FastAPI: Chosen for its speed, modern features, and ease of use when building RESTful APIs in Python.
- Docker: Used to containerize the application, ensuring consistent environments across different stages (development, testing, production).
- SQLAlchemy: Selected for its powerful ORM capabilities, enabling easy interaction with the PostgreSQL database while maintaining clean and maintainable code.
- Azure: 
    - Azure Storage Data Lake Gen2: Provides a scalable and secure file system for managing large data files, ensuring the project meets data storage and retrieval needs.
    - Azure Container App: Chosen for its flexibility and scalability, allowing the application to run smoothly in a cloud environment while providing robust support for containerized workloads.

### Security

The API is secured using Basic HTTP Authentication. All POST endpoints, including those for creating backups and restoring data, require authentication to ensure that only authorized users can access critical functionalities.

#### Authentication Details

- **Username:** Protected by environment variable `API_USERNAME`.
- **Password:** Protected by environment variable `API_PASSWORD`.

The authentication logic is handled by a dedicated module (`auth.py`) to maintain modularity and avoid circular dependencies. The credentials are compared using a secure method to prevent timing attacks, and are validated on every request.

To interact with the API, users must provide valid credentials via Basic Auth. This can be done easily through the Swagger UI or tools like Postman.

