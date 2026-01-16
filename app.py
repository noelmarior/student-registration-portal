import os
import psycopg2
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- CONFIGURATION ---
# 1. SECURITY KEY (Required for Sessions)
app.secret_key = 'change_this_to_something_random_and_secure'

# 2. Upload Config
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 3. Database Connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="student_portal",
        user="postgres",
        password="your_password_here"
    )
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # --- 1. DATA EXTRACTION ---
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    gender = request.form.get('gender', '')
    address = request.form.get('address', '').strip()
    stream = request.form.get('stream', '')
    course = request.form.get('course', '')

    # --- 2. BACKEND VALIDATION (The Firewall) ---
    
    # Check for empty fields
    if not all([name, email, phone, gender, address, stream, course]):
        return "Error: All fields are required."

    # Validate Email Format (Regex)
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return "Error: Invalid Email Format."

    # Validate Phone (Must be 10 Digits)
    if not phone.isdigit() or len(phone) != 10:
        return "Error: Phone number must be exactly 10 digits."

    # Validate Stream (Must be in our allowed list)
    valid_streams = ["Science", "Engineering", "Commerce", "Arts"]
    if stream not in valid_streams:
        return "Error: Invalid Stream selected."

    # --- 3. FILE HANDLING ---
    if 'photo' not in request.files: return "No file part"
    file = request.files['photo']
    if file.filename == '': return "No selected file"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo_path = f"uploads/{filename}"

        # --- 4. DATABASE INSERTION ---
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO students (name, email, phone, gender, address, stream, course, photo_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, phone, gender, address, stream, course, photo_path))
            conn.commit()
            cur.close()
            conn.close()
            # Success Page (Simple HTML return)
            return """
                <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
                    <h1 style="color: green;">Registered Successfully!</h1>
                    <p>Welcome to the college.</p>
                    <a href="/" style="text-decoration: none; background: #0d6efd; color: white; padding: 10px 20px; border-radius: 5px;">Go Back</a>
                </div>
            """
        except psycopg2.IntegrityError:
            conn.rollback()
            return "Error: This Email is already registered."
        except Exception as e:
            conn.rollback()
            return f"Database Error: {e}"
    
    return "Error: Invalid File Type (Only PNG, JPG, JPEG, GIF allowed)"

# --- AUTHENTICATION ROUTES (NEW) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # HARDCODED CREDENTIALS (Simple for now)
        if username == 'admin' and password == 'hellyeah987':
            session['logged_in'] = True
            return redirect('/admin')
        else:
            flash('Invalid Username or Password!')
            return redirect('/login')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

@app.route('/admin')
def admin():
    # THE GUARD: Check if user has the session card
    if not session.get('logged_in'):
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students;')
    students = cur.fetchall()
    cur.close()
    conn.close()
    
    # We pass the 'students' data AND a logout flag if needed
    return render_template('admin.html', students=students)

# --- NEW API ROUTE FOR LIVE CHECKING ---
@app.route('/check_value', methods=['POST'])
def check_value():
    data = request.get_json()
    field = data.get('field') # 'email' or 'phone'
    value = data.get('value')
    
    if not value:
        return jsonify({'exists': False})

    conn = get_db_connection()
    cur = conn.cursor()
    
    if field == 'email':
        cur.execute("SELECT id FROM students WHERE email = %s", (value,))
    elif field == 'phone':
        cur.execute("SELECT id FROM students WHERE phone = %s", (value,))
    
    result = cur.fetchone()
    cur.close()
    conn.close()

    # Returns True if found, False if not
    return jsonify({'exists': result is not None})

if __name__ == '__main__':
    app.run(debug=True)