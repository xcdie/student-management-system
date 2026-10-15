import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'f02488384727217f065be95be39a4a787e896243a61050f7e1794403e0e4a29c'


USERNAME = 'jamlick'
PASSWORD = '12345678'

def init_db():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/dashboard')

def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html')

@app.route('/add student'methods = ['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, email, course) VALUES (?, ?, ?)', (name, email, course))
        conn.commit()
        conn.close()

        flash('Student added successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_student.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('logout succesfuly')
    return redirect(url_for('login'))

if __name__ == '_main_':
    app.run(debug=True , port = 5001)
