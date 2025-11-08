from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "clavexdffdd"

USUARIOS_REGISTRADOS = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Por favor ingresa email y contraseña', 'error')
            return redirect(url_for('login'))

        if email not in USUARIOS_REGISTRADOS:
            flash('El usuario no existe', 'error')
            return redirect(url_for('login'))

        usuario = USUARIOS_REGISTRADOS[email]

        if usuario['password'] != password:
            flash('Contraseña incorrecta', 'error')
            return redirect(url_for('login'))

        session['usuario_email'] = email
        session['usuario_nombre'] = usuario['nombre']
        session['logueado'] = True

        flash(f'Bienvenido {usuario["nombre"]}!', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for('login'))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombres"]
        apellido = request.form["apellido"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        genero = request.form.get("genero")

        peso = request.form.get("peso")
        altura = request.form.get("altura")
        nivel_actividad = request.form.get("nivel_actividad")
        objetivo = request.form.get("objetivo")
        preferencias = request.form.get("preferencias")
        nivel_experiencia = request.form.get("nivel_experiencia")

        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
            return render_template("registro.html")

        if email in USUARIOS_REGISTRADOS:
            flash("Este correo ya está registrado", "error")
            return render_template("registro.html")

        USUARIOS_REGISTRADOS[email] = {
            "nombre": nombre,
            "apellido": apellido,
            "fecha_nacimiento": fecha_nacimiento,
            "genero": genero,
            "peso": peso,
            "altura": altura,
            "nivel_actividad": nivel_actividad,
            "objetivo": objetivo,
            "preferencias": preferencias,
            "nivel_experiencia": nivel_experiencia,
            "password": password
        }

        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/educacion")
def educacion():
    return render_template("Educacion.html")


if __name__ == "__main__":
    app.run(debug=True)
