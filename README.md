Student Registration Portal

A full-stack web application for college student registrations. Built with **Python Flask**, **PostgreSQL**, and **Bootstrap 5**.

🚀 Features
- **Student Registration Form:** Collects personal details, academic info, and photos.
- **Real-time Validation:** Instantly checks if an Email or Phone number is already registered (AJAX).
- **Dynamic Dropdowns:** Course options change automatically based on the selected Stream.
- **Admin Dashboard:** Secure, password-protected panel to view all registrations.
- **Data Integrity:** Prevents duplicate entries and ensures valid data formats.

🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (Fetch API)
- **Backend:** Python 3, Flask
- **Database:** PostgreSQL

⚙️ Setup Instructions

1. Clone the Repository
git clone [https://github.com/YOUR_USERNAME/student-registration-portal.git](https://github.com/YOUR_USERNAME/student-registration-portal.git)
cd student-registration-portal

2. Install Dependencies
   pip install flask psycopg2-binary

3. Database Setup (PostgreSQL)
   Log in to your Postgres shell and run these commands to create the database and table:
   CREATE DATABASE student_portal;
   \c student_portal
   CREATE TABLE students (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       phone VARCHAR(20) NOT NULL,
       gender VARCHAR(10) NOT NULL,
       address TEXT NOT NULL,
       stream VARCHAR(50) NOT NULL,
       course VARCHAR(50) NOT NULL,
       photo_path TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

4. Configure Application
   Open app.py and update the database connection with your local PostgreSQL password:
   conn = psycopg2.connect(
       host="localhost",
       database="student_portal",
       user="postgres",
       password="YOUR_DB_PASSWORD" 
   )

5. Run the Server
   python app.py
   Access the application at: http://127.0.0.1:5000

To view the registered students, go to /admin.
Username: admin
Password: hellyeah987
