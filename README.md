# Task Manager

A simple task management application built with Django and Django REST Framework. This project includes user authentication and CRUD operations for tasks, with frontend for a seamless user experience.

## Features

- User registration and login
- Create, view, update, and delete tasks
- Responsive UI with Bootstrap

## Prerequisites

- Python 3.x
- Django 3.x
- Django REST Framework
- jQuery

## Setup Instructions

### 1. Clone the Repository

```bash
1. git clone https://github.com/dixitshweta17/taskmanager.git
2. cd taskmanager
3. activate virtual environment ()
4. pip install -r requirements.txt
5. apply migrations by using following commands
    python manage.py makemigrations
    python manage.py migrate
6. create the superuser for django admin access
    python manage.py createsuperuser
7. run the server now
    python manage.py runserver


Make sure to adjust the paths, URLs, and any other specifics to match your project setup. This `README.md` provides a comprehensive overview and instructions for setting up and using the project.

urls for refference:
User Registrations: BASEURL/user/register/
User Login : BASEURL/user/login/
TASK LIST : BASEURL/tasks/
Task Create: BASEURL/tasks/tasks/create/
Task Update: BASEURL/tasks/<task_id>/

