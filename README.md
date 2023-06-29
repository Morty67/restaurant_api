# Lunch Decision Backend
This project aims to develop a backend service for an internal lunch decision-making system. The system allows employees to vote for their preferred menu at different restaurants before heading out for lunch. The backend will be responsible for handling user authentication, restaurant management, menu uploading, employee registration, and providing information about the current day's menu and voting results.

🖥️ Tech Stack
The project will be developed using the following technologies:
: Django + DRF, JWT, PostgreSQL, Docker(docker-compose), PyTests;

## Installing / Getting started:
```shell
To get started, you need to clone the repository from GitHub: https://github.com/Morty67/restaurant_api/
Python 3 must be installed

python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

pip install -r requirements.txt

Your settings for DB in .env file:
POSTGRES_DB=<POSTGRES_DB>
POSTGRES_USER=<POSTGRES_USER>
POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
POSTGRES_HOST=<POSTGRES_HOST>
SECRET_KEY=<YOUR DJANGO SECRET_KEY>

python manage.py migrate
python manage.py runserver
```

## Run Docker 🐳
Docker must be installed 
```shell
* docker-compose up --build
* docker exec -it ********* python manage.py createsuperuser {********* - id your container}
```

## How to get access

Domain:
*  localhost:8000
*  create new user - api/user/register/
*  get JWT Token - api/user/token/

## Features:

*  Admin panel - admin/
*  Documentation is located at api/doc/swagger/
*  Authentication: The backend will provide authentication mechanisms to ensure secure access to the system's features.
*  Restaurant Management: The system supports the creation of new restaurants, allowing them to upload their menus via an API (Only users with the is_staff: True attribute are allowed to create, delete, and modify restaurants).
*  Menu Upload: Restaurants can upload menus for each day, ensuring employees have up-to-date information (Only users with the is_staff: True attribute are allowed to create, delete, and modify menus).
*  Employee Registration: Employees can create accounts and participate in the voting process.
*  Current Day Menu: The backend provides an endpoint to fetch the menu for the current day, allowing employees to view available options (Employees can view all available menus for the current day).
*  Voting Results: The backend provides an endpoint to retrieve the voting results for the current day, helping employees make informed decisions (The top 3 menus based on voting results are displayed).
*  To check the version using Postman, the version can be passed in the headers./ Get - http://127.0.0.1:8000/api/rest/result/ Key-Accept  Value-application/json; version=2.0 (or 1.0) Two different versions of the application will showcase different functionalities.
*  To check the version using Postman, the version can be passed in the headers. / Post http://127.0.0.1:8000/api/rest/votes/ Key-Accept  Value-application/json; version=2.0 (or 1.0) and Key-Authorization Value-Bearer(<your JWT>) Two different versions of the application will showcase different functionalities.