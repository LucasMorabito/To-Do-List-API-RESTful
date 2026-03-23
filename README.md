# To-Do List API

A RESTful API for task management built with Django REST Framework. Features JWT authentication, task filtering, search, pagination, and interactive API documentation via Swagger.

**Live API:** https://to-do-list-api-restful.onrender.com  
**Interactive Docs:** https://to-do-list-api-restful.onrender.com/api/docs/

---

## Tech Stack

- **Python** / **Django 6** / **Django REST Framework**
- **PostgreSQL** (production) / SQLite (development)
- **JWT Authentication** via `djangorestframework-simplejwt`
- **Swagger / OpenAPI** documentation via `drf-spectacular`
- **Deployed on Render**

---

## Features

- JWT-based authentication (register, login, token refresh)
- Full CRUD for tasks
- Filter tasks by completion status and priority
- Search tasks by title or description
- Order tasks by creation date or due date
- Pagination (10 tasks per page)
- Per-user data isolation — users only see their own tasks
- Interactive API documentation (Swagger UI)
- Automated test suite

---

## Getting Started

### Prerequisites

- Python 3.12+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/LucasMorabito/To-Do-List-API-RESTful.git
cd To-Do-List-API-RESTful

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your-secret-key-here
```

To generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/api/register/` | Create a new user account | No |
| POST | `/api/login/` | Obtain JWT access and refresh tokens | No |
| POST | `/api/refresh/` | Refresh an expired access token | No |

### Tasks

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks/` | List all tasks for the authenticated user | Yes |
| POST | `/api/tasks/` | Create a new task | Yes |
| GET | `/api/tasks/{id}/` | Retrieve a specific task | Yes |
| PUT | `/api/tasks/{id}/` | Update a task (full update) | Yes |
| PATCH | `/api/tasks/{id}/` | Update a task (partial update) | Yes |
| DELETE | `/api/tasks/{id}/` | Delete a task | Yes |

### Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/docs/` | Swagger UI — interactive API documentation |
| GET | `/api/schema/` | OpenAPI schema (JSON) |

---

## Query Parameters

Tasks support filtering, searching, and ordering via query parameters:

```
GET /api/tasks/?completed=false              # Only pending tasks
GET /api/tasks/?priority=high                # Only high priority tasks
GET /api/tasks/?completed=false&priority=high  # Pending AND high priority
GET /api/tasks/?search=groceries             # Search in title and description
GET /api/tasks/?ordering=due_date            # Order by due date (ascending)
GET /api/tasks/?ordering=-created_at         # Order by creation date (descending)
GET /api/tasks/?page=2                       # Page 2 (10 tasks per page)
```

**Priority values:** `low`, `medium`, `high`

---

## Request & Response Examples

### Register

```
POST /api/register/
Content-Type: application/json

{
    "username": "lucas",
    "password": "securepassword123",
    "email": "lucas@example.com"
}
```

```json
{
    "message": "User created successfully"
}
```

### Login

```
POST /api/login/
Content-Type: application/json

{
    "username": "lucas",
    "password": "securepassword123"
}
```

```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Create a Task

```
POST /api/tasks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "medium",
    "due_date": "2025-12-31T18:00:00Z"
}
```

```json
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "priority": "medium",
    "due_date": "2025-12-31T18:00:00Z",
    "created_at": "2025-03-23T12:00:00Z",
    "user": 1
}
```

### List Tasks (paginated response)

```
GET /api/tasks/
Authorization: Bearer <access_token>
```

```json
{
    "count": 25,
    "next": "https://to-do-list-api-restful.onrender.com/api/tasks/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "priority": "medium",
            "due_date": "2025-12-31T18:00:00Z",
            "created_at": "2025-03-23T12:00:00Z",
            "user": 1
        }
    ]
}
```

---

## Task Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Auto-generated unique identifier |
| `title` | string | Task title (max 200 characters) |
| `description` | string | Task description |
| `completed` | boolean | Completion status (default: false) |
| `priority` | string | `low`, `medium`, or `high` (default: medium) |
| `due_date` | datetime | Optional due date |
| `created_at` | datetime | Auto-set on creation |
| `user` | integer | Owner of the task (set automatically) |

---

## Running Tests

```bash
pytest
```

The test suite covers:

- Unauthenticated users cannot access tasks (returns 401)
- Authenticated users can access their tasks
- Users cannot see other users' tasks
- User registration via API
- Token generation after login
- Task creation and persistence
- Task isolation between users
- Task update (PATCH)

---

## Project Structure

```
To-Do-List-API-RESTful/
├── ToDoAPI/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Lists/
│   ├── api.py          # Views
│   ├── models.py       # Task model
│   ├── serializers.py  # TaskSerializer, RegisterSerializer
│   ├── urls.py         # App URL routing
│   └── migrations/
├── Tests/
│   ├── test_auth.py    # Authentication tests
│   └── test_task.py    # Task tests
├── requirements.txt
└── manage.py
```

---

## Author

**Lucas Morabito**  
[GitHub](https://github.com/LucasMorabito) · [LinkedIn](https://linkedin.com/in/lucasmorabito)

---

## License

This project is open source and available under the [MIT License](LICENSE).
