# TaskForge

## Overview

TaskForge is a task and workflow management
web application. The main objective is helping teams track projects and manage tickets and bug reports.

### Features

- **Project Management**: Create and manage projects with descriptions and team assignments
- **Ticket System**: Track tasks and bug reports with priority levels and status updates
- **Bug Tracking**: Dedicated bug reporting system with approval workflow
- **Team Collaboration**: Comment system on tickets
- **Role-Based Access**: Different permission levels for managers, developers, and end users
- **Analytics Dashboard**: Visual insights into project progress and team workload
- **Dark/Light Mode**: Support for both dark and light themes
- **Responsive Design**: Works on desktop and mobile devices

#### User Roles

- **End Users**: Can create bug reports and view projects that they are part of
- **Developers**: Have full CRUD over their own tickets, and can only Edit assigned tickets
- **Project Managers**: Have full CRUD over projects, tickets and bug reports, can approve bug reports
- **Administrators**: Have full system control

#### Built with:

- Django
- PostgreSQL
- Bootstrap
- Plotly - Data visualization
- Django Template Engine - Frontend templating

#### Requirements:

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Gmail with 2FA enabled and App pass

### Installation

1. Clone the repo and create a python virtual environment.
2. Install dependencies:

~~~code
pip install -r requirements.txt
~~~

3. Setup your PostgreSQL db
4. Create a '.env' file with the following variables:

~~~code
SECRET_KEY=your_secret_key_here
DEBUG=True 
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_app_password
~~~

5. Run migrations

```code
python manage.py migrate
```

6. Create superuser and run django's development server.

```code
python manage.py createsuperuser
python manage.py runserver
```

7. Project runs on:
   `http://localhost:8000`

### Testing
Run the Django testing tool:
```code
python manage.py test
```

### Disclaimer

This project was created as part of my thesis work for
Python Web course at SoftUni.
It is intended for academic use only and is not for commercial purposes.