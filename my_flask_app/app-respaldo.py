from flask import Flask, render_template, request, redirect, url_for, session, flash
from connection import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto a una clave secreta real

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Aquí puedes agregar la lógica para validar las credenciales
        # Por ejemplo, comparar con valores de una base de datos
        if username == 'admin' and password == 'admin':  # Ejemplo sencillo
            session['username'] = username
            return redirect(url_for('index.html'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT Id, Value, Date FROM Temperature')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
