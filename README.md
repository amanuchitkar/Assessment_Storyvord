# Task Management API

A simple Task Management API built with Django and Django Rest Framework.

## Features

- User Authentication with JWT
- CRUD operations for tasks
- Task filtering by completion status and date ranges
- Pagination
- Custom permissions
- Admin interface

## Requirements

- Python 3.8+
- Django 5.1+
- Django REST Framework 3.15+
- Other dependencies in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd task_manager
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `GET /api/tasks/` - List all tasks (admin users see all tasks, regular users see only their own)
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Get details of a specific task
- `PUT /api/tasks/{id}/` - Update a task
- `PATCH /api/tasks/{id}/` - Partially update a task
- `DELETE /api/tasks/{id}/` - Delete a task

## Filtering Tasks

- Filter by completion status: `/api/tasks/?completed=true`
- Filter by creation date: `/api/tasks/?created_after=2024-01-01`
- Filter by update date: `/api/tasks/?updated_after=2024-01-01`

## Authentication

The API uses JWT authentication. To authenticate:

1. Obtain a token by sending a POST request to `/api/token/` with your username and password.
2. Include the token in the Authorization header of your requests:
   `Authorization: Bearer <your-token>`

## Permissions

- Only authenticated users can access the API
- Users can only update or delete their own tasks
- Admin users can view all tasks, regular users can only view their own tasks 