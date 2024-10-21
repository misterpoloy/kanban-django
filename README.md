
# README.md

This project implements a simple Kanban board backend using Django with GraphQL and JWT authentication. The backend manages boards, columns, and cards, with user-specific data access.

**by Juan P. Ortiz**

![Banner](./images/banner.png)

## Prerequisites  
- Python 3.x installed on your machine.  
- Virtual environment tool (venv).  
- DynamoDB Local installed (for future persistence).  
- Postman or GraphiQL for testing GraphQL queries.  
- Node.js (optional) if you plan to extend to the frontend later.  
- Docker and Docker Compose installed.

---

## Virtual Environment Setup (Optional for Local Development)

### Activate a Virtual Environment  

```
python3 -m venv venv  
source venv/bin/activate  # Mac/Linux  
venv\Scriptsctivate  # Windows  
```

### Install Dependencies  
Make sure you are inside the project directory:

```
pip install -r requirements.txt  
```

### Apply Migrations  

```
python manage.py migrate  
```

## Create a Superuser  
You need a superuser to test authentication and manage users:

```
python manage.py createsuperuser  
```

Follow the prompts to create the superuser with username, password, and email.

## Run Dev Server  

```
python manage.py runserver  
```

---

## GraphQL Authentication

### Obtain a JWT Token  
Send a POST request to `/api/token/` using Postman or cURL:

**Request:**  

```
curl -X POST http://127.0.0.1:8000/api/token/ \  
-H "Content-Type: application/json" \  
-d '{"username": "your_username", "password": "your_password"}'  
```

**Expected Response:**  
```json
{
  "access": "<your_jwt_access_token>",  
  "refresh": "<your_jwt_refresh_token>"  
}
```  

Use the access token for authenticated requests.

---

## Access GraphQL Endpoint  
Open GraphiQL at:  

```
http://127.0.0.1:8000/graphql/  
```

Add the following headers:

```json
{
  "Authorization": "Bearer <your_jwt_access_token>"  
}
```

---

## Example Query  

Use the following query to retrieve user-specific boards:

```graphql
{
  boards {  
    columns {  
      title  
      cards {  
        content  
      }  
    }  
  }  
}
```

---

## Project Structure  

```
kanban_project/  
│  
├── kanban/              # Main app folder  
│   ├── migrations/      # Django migrations folder  
│   ├── models.py        # Data models for Card, Column, and Board  
│   ├── schema.py        # GraphQL schema and resolvers  
│   └── views.py         # Custom GraphQL view for JWT authentication  
│  
├── manage.py            # Django management script  
├── requirements.txt     # Python dependencies  
└── README.md            # Project documentation  
```

---

## Start DynamoDB  

```
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb  
```

---

## Docker Setup  

### Backend Dockerfile  

Create a **Dockerfile** inside the `kanban-backend/` folder:

```
FROM python:3.9-slim  
WORKDIR /app  
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  
COPY . .  
EXPOSE 8000  
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]  
```

---

### Docker Compose Configuration  
Make sure you are in the root directory

```
docker-compose up --build  
```

---

## Troubleshooting  

**Token Expired:**  
Request a new access token using `/api/token/`.  

**Authentication Error:**  
Ensure the Authorization header is correctly formatted:  
```
Bearer <your_jwt_access_token>  
```

**GraphQL Query Error:**  
> Note: Remember to create the inital columns at the beguining and the power user to login

Ensure your GraphQL queries follow the correct schema. Example for creating a new column:

```graphql
mutation {  
  createColumn(title: "To Do") {  
    column {  
      id  
      title  
    }  
  }  
}
```

Use similar queries to create **In Progress** and **Done** columns.

---

This README now includes instructions for **Docker** setup with **Docker Compose** to manage the backend service.
