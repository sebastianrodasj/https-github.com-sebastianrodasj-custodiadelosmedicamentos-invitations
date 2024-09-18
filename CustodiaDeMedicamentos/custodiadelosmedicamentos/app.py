from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'custodiadelosmedicamentos'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Ruta para la página principal (login)
@app.route('/')
def index():
    return render_template('login.html')

# Ruta para manejar el login
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s", (usuario, contrasena))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Usuario autenticado correctamente
            flash('Inicio de sesión exitoso', 'success')
            return redirect('/')
        else:
            # Usuario o contraseña incorrecta
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect('/')

# Ruta para registrar un nuevo usuario
@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        nombre_usuario = request.form['usuario']
        contrasena = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s)", (nombre_usuario, contrasena))
        mysql.connection.commit()
        cursor.close()

        flash('Usuario registrado con éxito', 'success')
        return redirect('/')

# Función principal para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
