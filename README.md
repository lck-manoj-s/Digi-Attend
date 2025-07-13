# Digi Attend

## Table of Contents
- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)

## Overview
Digi Attend is a comprehensive attendance portal built on the Django framework, designed to streamline attendance tracking and administrative workflows within educational institutions. It features a modular architecture with dedicated apps for attendance, user management, and administrative functions, all styled with Bootstrap for a polished user experience.

## Technology Stack
### 1. 💻 Frontend
- **Bootstrap CSS** – Utility-first CSS framework for styling.

- **JavaScript (ES6+)** – Core scripting language.

### 2. 🌐 Backend
- **Django** – Python web framework with wide array of built-in tools and components for common web development tasks.

### 3. 🛢️ Database
- **MySQL** – SQL database to store all the data in a tabular form.

- **Django ORM** – ORM to define schemas and interact with MySQL easily.

## Features
This project aims to provide a scalable, secure, and easy-to-maintain solution for managing attendance,
staff, and student data. The core features include:

- **Role-Based Access Control**: Ensures secure navigation with custom middleware and
authentication backends.

- **Responsive UI Templates**: Offers dynamic dashboards for staff, students, and admins, enhancing
usability.

- **Real-Time Attendance & Leave Management**: Facilitates accurate tracking and streamlined leave
workflows.

- **Seamless Deployment**: Integrates with Django management commands for easy setup and

maintenance.

- **Extensible Architecture**: Supports future enhancements with a modular, organized codebase.
  
## Project Structure
```
system/
├── attendance/
│   ├── templates/
│   │   ├── hod_template/
│   │   ├── student_template/
│   │   ├── staff_template/
│   │   ├── registration/
│   │   └── login.html
│   ├── forms.py
│   ├── LoginCheckMiddleware.py
│   ├── EmailBackEnd.py
│   ├── models.py
│   ├── staffviews.py
│   ├── hodviews.py
│   ├── studentviews.py
│   └── views.py
├── system/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```
### Backend
- `forms.py`: Used to contain forms to edit & add Student data.
- `LoginCheckMiddleware.py`: Used for role-based authentication & re-direction to respective home pages.
- `models.py`: Defines the data models that are used to store the data at backend relational tables.
- `staffviews.py`: Contains all the functions with respective to staff role.
- `studentviews.py`: Contains all the functions with respective to student role.
- `hodviews.py`: Contains all the functions with respective to HOD/admin role.
- `views.py`: Contains all the functions for the generic login & logouts.
- `EmailBackEnd.py`: Used to fetch the login credentails for the users.

### Frontend
- `hod_template/`: Contains all the html files related to HOD/admin role.
- `student_template/`: Contains all the html files related to student role.
- `staff_template/`: Contains all the html files related to staff role.
- `registration/`: Contains all the html files related to logins, reset password and others.
- `login.html`: Holds the content to display the login page.
  
## Installation
### 1. Clone the repository
`git clone https://github.com/yourusername/Digi-Attend.git`

### 2. Install Necessary Dependencies
Make sure to have Python installed in the system. After python has been successfully installed, install the dependencies from requirements.txt
```
pip install requirements.txt
```

## Usage
### 1. Start the Django server
```
python manage.py runserver
```

