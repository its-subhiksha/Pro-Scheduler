# Pro-Scheduler Appointment Booking API

This is a simple appointment scheduling API built with Django, created as part of an interview assignment. It allows service providers to set their available time slots and lets clients book appointments during those times without causing overlaps.

---

## 🚀 Tech Stack

* Python 3.10+
* Django & Django REST Framework
* PostgreSQL

---

## ✅ Features

* Add and manage providers
* Add provider availability time blocks
* Book appointments in available time slots
* Handles conflicts to prevent double bookings
* Dynamically shows open slots excluding existing bookings

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pro-scheduler.git
cd pro-scheduler
```

### 2. Set Up Virtual Environment

```bash
python -m venv env
env\Scripts\activate  # For Windows
# or
source env/bin/activate  # For Mac/Linux
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

Update your `.env` or `settings.py` with:

```env
DB_NAME=pro_scheduler_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

Then run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

### 6. (Optional) Create an Admin Superuser

```bash
python manage.py createsuperuser
```

---

## 🧠 Design Notes

* Django was chosen for its stability and built-in admin interface.
* DRF simplifies creating and testing REST APIs.
* PostgreSQL supports safe row locking which helps prevent race conditions.

---

## 🔐 Handling Race Conditions

The booking system uses database transactions to avoid double-booking:

* `transaction.atomic()` ensures atomicity.
* `select_for_update()` locks overlapping appointments.
* Any attempt to book an already-reserved slot will return a conflict.

---

## 🔗 API Endpoints

### ➕ Create Provider

```
POST /api/providers/
{
  "name": "Dr. Smith"
}
```

### ➕ Add Availability

```
POST /api/providers/1/availability
{
  "start_time": "2025-07-15T09:00:00Z",
  "end_time": "2025-07-15T11:00:00Z"
}
```

### 📅 View Open Time Slots

```
GET /api/providers/1/availability/slots?duration=30
```

### 📌 Book an Appointment

```
POST /api/appointments
{
  "provider": 1,
  "client_name": "John Doe",
  "start_time": "2025-07-15T09:00:00Z",
  "end_time": "2025-07-15T09:30:00Z"
}
```

### 📋 List All Booked Appointments

```
GET /api/providers/1/appointments
```

---

## 📌 Assumptions Made

* Timestamps are in **UTC**
* Clients are identified only by name
* The app does not require login or auth (as per task spec)
* The system accepts arbitrary appointment durations

---

## ⚡ Performance Notes

To keep things responsive:

```python
class Meta:
    indexes = [
        models.Index(fields=["provider", "start_time"])
    ]
```

This speeds up queries involving slot searches and overlaps.

---

## 📁 Project Structure

```
pro_scheduler/
├── scheduler/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
├── pro_scheduler/
│   └── settings.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```


## 🧼 .gitignore

```gitignore
__pycache__/
*.pyc
env/
*.sqlite3
*.log
.DS_Store
*.env
*.vscode
```

---

## ✅ Final Notes

This project was created to solve a real-world appointment scheduling problem with simplicity and reliability. The logic is built to be easily testable, scalable, and safe from common concurrency issues.

Thanks for reviewing the code!
