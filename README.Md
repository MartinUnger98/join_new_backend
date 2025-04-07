# 🧠 Join Backend API

A clean, modular backend built with Django and Django REST Framework, designed for task and contact management. Features user authentication, guest login, and nested subtasks using clean code principles.

---

## 🚀 Features

- ✅ Token-based authentication (login, guest login)
- ✅ User registration
- ✅ CRUD for Contacts
- ✅ CRUD for Tasks with nested Subtasks
- ✅ Modular structure with clean code principles (PEP-8, single responsibility, utils)
- ✅ Fully RESTful API

---

## 🏗️ Tech Stack

- Python 3.12+
- Django 5.2
- Django REST Framework
- SQLite (default, configurable)
- TokenAuthentication

---

## 📦 Installation

```bash```
git clone https://github.com/MartinUnger98/join_new_backend.git
cd join-backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

---

## ⚙️ Configuration

Make sure your `.env` file exists at the root of the project with the following content:

```env```
GUEST_USERNAME=guest_user
GUEST_PASSWORD=guest123
GUEST_EMAIL=guestLogin@guest.com

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional: to access Django admin

---

## ▶️ Run the Server
python manage.py runserver
Open your browser at: http://localhost:8000

---

## 🛠️ API Endpoints

## 🔐 Auth
Method	Endpoint	Description
POST	/login/	User login (returns token)
POST	/guest-login/	Logs in guest user
POST	/register/	Register a new user

## 👤 Contacts
Method	Endpoint	Description
GET	/contacts/	List all contacts
POST	/contacts/	Create a new contact
PUT	/contacts/<id>/	Update contact
DELETE	/contacts/<id>/	Delete contact

## ✅ Tasks & Subtasks
Method	Endpoint	Description
GET	/tasks/	List all tasks
POST	/tasks/	Create task with subtasks
PUT	/tasks/<id>/	Update task and subtasks
DELETE	/tasks/<id>/	Delete task

---

## 🧼 Code Style & Structure
This project follows clean code and Django best practices:

✅ Follows PEP-8

✅ Uses snake_case for all variables and field names

✅ Every function/method does only one thing

✅ Functions are max. 14 lines long

✅ No commented or unused code

✅ Utility logic (e.g. subtask syncing) is moved to utils.py