from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'Miguel@123'

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicialización de la base de datos
def init_db():
    if not os.path.exists('database.db'):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# Página de inicio (bienvenida)
@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))

# Registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if not username or not email or not password:
            flash('Por favor, completa todos los campos.', 'error')
        elif len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'error')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                         (username, email, generate_password_hash(password)))
            conn.commit()
            conn.close()
            flash('Te has registrado exitosamente!', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

# Inicio de sesión de usuarios
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas.', 'error')
    
    return render_template('login.html')

# Página del juego
@app.route('/game')
def game():
    if 'user_id' in session:
        return render_template('game.html')
    return redirect(url_for('login'))

# Cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()  # Inicializar la base de datos si no existe
    app.run(debug=True)
