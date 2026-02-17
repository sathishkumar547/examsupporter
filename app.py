from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sathish12',
    'database': 'student_exam_supporter'
}

# File upload configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

bcrypt = Bcrypt(app)

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create materials table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                subject VARCHAR(100) NOT NULL,
                university VARCHAR(100) NOT NULL,
                type VARCHAR(50) NOT NULL,
                filename VARCHAR(255) NOT NULL,
                file_path VARCHAR(255) NOT NULL,
                user_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Check if subject column exists, if not add it
        try:
            cursor.execute("ALTER TABLE materials ADD COLUMN subject VARCHAR(100) NOT NULL AFTER title")
            conn.commit()
            print("Added subject column to materials table")
        except:
            pass  # Column already exists
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database tables created successfully!")

# Routes

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)',
                             (name, email, hashed_password))
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except Error as e:
                if 'Duplicate entry' in str(e):
                    flash('Email already registered!', 'danger')
                else:
                    flash(f'Error: {str(e)}', 'danger')
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Database connection failed!', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user and bcrypt.check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_email'] = user['email']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password!', 'danger')
        else:
            flash('Database connection failed!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to access the dashboard!', 'warning')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    materials_count = 0
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM materials WHERE user_id = %s', (session['user_id'],))
        materials_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    
    return render_template('dashboard.html', materials_count=materials_count)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        flash('Please login to upload materials!', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        subject = request.form['subject']
        university = request.form['university']
        material_type = request.form['type']
        
        if 'file' not in request.files:
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected!', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Save to database
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                        INSERT INTO materials (title, subject, university, type, filename, file_path, user_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (title, subject, university, material_type, filename, file_path, session['user_id']))
                    conn.commit()
                    flash('File uploaded successfully!', 'success')
                    return redirect(url_for('materials'))
                except Error as e:
                    flash(f'Error saving to database: {str(e)}', 'danger')
                finally:
                    cursor.close()
                    conn.close()
            else:
                flash('Database connection failed!', 'danger')
        else:
            flash('Invalid file type! Only PDF files are allowed.', 'danger')
    
    return render_template('upload.html')

@app.route('/materials')
def materials():
    if 'user_id' not in session:
        flash('Please login to view materials!', 'warning')
        return redirect(url_for('login'))
    
    # Get search parameters
    university = request.args.get('university')
    subject = request.args.get('subject')
    
    conn = get_db_connection()
    materials_list = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if university and subject:
            # Filter by both university and subject (search in subject field)
            subject_pattern = f"%{subject}%"
            cursor.execute('''
                SELECT m.*, u.name as uploaded_by 
                FROM materials m 
                JOIN users u ON m.user_id = u.id 
                WHERE m.university = %s AND m.subject LIKE %s
                ORDER BY m.created_at DESC
            ''', (university, subject_pattern))
        elif university:
            # Filter by university only
            cursor.execute('''
                SELECT m.*, u.name as uploaded_by 
                FROM materials m 
                JOIN users u ON m.user_id = u.id 
                WHERE m.university = %s
                ORDER BY m.created_at DESC
            ''', (university,))
        else:
            # Show all materials
            cursor.execute('''
                SELECT m.*, u.name as uploaded_by 
                FROM materials m 
                JOIN users u ON m.user_id = u.id 
                ORDER BY m.created_at DESC
            ''')
        
        materials_list = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template('materials.html', materials=materials_list, search_university=university, search_subject=subject)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please login to view profile!', 'warning')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, name, email, created_at FROM users WHERE id = %s', (session['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    
    if request.method == 'POST':
        name = request.form['name']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT password FROM users WHERE id = %s', (session['user_id'],))
            user_data = cursor.fetchone()
            
            if bcrypt.check_password_hash(user_data['password'], current_password):
                hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                cursor.execute('UPDATE users SET name = %s, password = %s WHERE id = %s',
                             (name, hashed_new_password, session['user_id']))
                conn.commit()
                session['user_name'] = name
                flash('Profile updated successfully!', 'success')
            else:
                flash('Current password is incorrect!', 'danger')
            
            cursor.close()
            conn.close()
        
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user)

@app.route('/view/<filename>')
def view_file(filename):
    if 'user_id' not in session:
        flash('Please login to view files!', 'warning')
        return redirect(url_for('login'))
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
