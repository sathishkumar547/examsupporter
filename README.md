# Student Exam Supporter

A full-stack web application for students to upload and share exam study materials like important questions, old question papers, and book references.

## Features

- **Authentication System**: Student registration and login with password hashing
- **Dashboard**: Clean modern UI with quick access to all features
- **Upload Materials**: Upload PDF files (max 10MB) with title, university, and material type
- **View Materials**: Browse materials in card format with "View" button to open PDFs
- **Profile Management**: View and edit profile details, change password

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: MySQL
- **Password Hashing**: Bcrypt

## Project Structure

```
student-exam-supporter/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── config.py                 # Configuration file
├── database/
│   └── schema.sql           # MySQL database schema
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   └── uploads/             # Uploaded PDF files (created automatically)
└── templates/
    ├── base.html            # Base template
    ├── login.html           # Login page
    ├── register.html        # Registration page
    ├── dashboard.html       # Dashboard page
    ├── upload.html          # Upload materials page
    ├── materials.html       # View materials page
    └── profile.html         # Profile page
```

## Prerequisites

1. **Python 3.8+** installed
2. **MySQL** installed and running
3. **XAMPP** or **WAMP** (optional, for MySQL management)

## Installation & Setup

### Step 1: Install Python Dependencies

Open your terminal/command prompt and run:

```
bash
pip install -r requirements.txt
```

### Step 2: Setup MySQL Database

1. Open MySQL (via XAMPP/WAMP or command line)
2. Create the database by running:

```
bash
mysql -u root -p < database/schema.sql
```

Or manually create the database:

```
sql
CREATE DATABASE student_exam_supporter;
USE student_exam_supporter;

-- Then run the SQL commands from database/schema.sql
```

### Step 3: Configure Database Connection

Open `app.py` and update the DB_CONFIG dictionary with your MySQL credentials:

```
python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Change this to your MySQL password
    'database': 'student_exam_supporter'
}
```

**Note**: If using XAMPP, the default MySQL password is usually empty ( '' ). If using MySQL without password, set `'password': ''`.

### Step 4: Run the Application

```
bash
python app.py
```

### Step 5: Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage

1. **Register**: Create a new account by clicking "Register here" on the login page
2. **Login**: Use your email and password to login
3. **Dashboard**: View your dashboard with quick stats and navigation
4. **Upload Materials**: Go to "Upload Materials" to share study materials
5. **View Materials**: Browse all uploaded materials in the "View Materials" page
6. **Profile**: Update your name and change password in the "Profile" page
7. **Logout**: Click "Logout" to end your session

## Database Tables

### users table
| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Auto-increment primary key |
| name | VARCHAR(100) | User's full name |
| email | VARCHAR(100) | Unique email address |
| password | VARCHAR(255) | Hashed password |
| created_at | TIMESTAMP | Account creation time |

### materials table
| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Auto-increment primary key |
| title | VARCHAR(200) | PDF title |
| university | VARCHAR(100) | University name |
| type | VARCHAR(50) | Material type (Important Questions / Old Question Paper / Book Reference) |
| filename | VARCHAR(255) | Saved filename |
| file_path | VARCHAR(255) | Path to file |
| user_id | INT (FK) | Reference to users.id |
| created_at | TIMESTAMP | Upload time |

## Troubleshooting

### MySQL Connection Error
- Make sure MySQL is running
- Check username and password in DB_CONFIG
- Verify the database exists

### File Upload Error
- Ensure the `static/uploads` folder exists and has write permissions
- Check file size (max 10MB)
- Only PDF files are allowed

### Port Already in Use
If port 5000 is busy, modify the last line in app.py:
```
python
app.run(debug=True, port=5001)  # Change to a different port
```

## License

This project is for educational purposes.
