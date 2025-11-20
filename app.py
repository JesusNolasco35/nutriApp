from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "clavexdffdd"

USUARIOS_REGISTRADOS = {}


@app.route('/')
def bienvenida():
    """
    Página de bienvenida.
    Ofrece opciones de registrarse, iniciar sesión o continuar como invitado.
    """
    return render_template("bienvenida.html")



@app.route('/inicio')  
def index():
    """
    Página principal de NutriApp después de iniciar sesión o entrar como invitado.
    """
    return render_template("index.html")


@app.route('/inicio_invitado')
def inicio_invitado():
    """
    Permite entrar como invitado sin necesidad de registrarse ni iniciar sesión.
    Redirige al mismo index pero con flag de invitado si quieres mostrar algo especial.
    """
    session['logueado'] = False  
    return redirect(url_for('index'))


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

@app.route("/ajustes")
def ajustes():
    return render_template("ajustes.html")

@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")

from flask import Flask, render_template, request, redirect, url_for, flash, session


@app.route("/imc", methods=["GET", "POST"])
def imc():
    if request.method == "POST":
        try:
            peso = float(request.form.get("peso"))
            altura = float(request.form.get("altura")) / 100  

            if peso <= 0 or altura <= 0:
                flash("Los valores deben ser mayores a 0.", "error")
                return redirect(url_for("imc"))

            imc_valor = peso / (altura ** 2)

            if imc_valor < 18.5:
                estado = "Bajo peso"
            elif imc_valor < 25:
                estado = "Normal"
            elif imc_valor < 30:
                estado = "Sobrepeso"
            else:
                estado = "Obesidad"

            flash(f"Tu IMC es {imc_valor:.2f} — {estado}", "success")
            return redirect(url_for("imc"))

        except ValueError:
            flash("Por favor ingresa números válidos.", "error")
            return redirect(url_for("imc"))

    return render_template("imc.html")


@app.route("/tmb", methods=["GET", "POST"])
def TMB():
    if request.method == "POST":
        try:
            edad = float(request.form["edad"])
            peso = float(request.form["peso"])
            altura = float(request.form["altura"])
            sexo = request.form["sexo"]

            
            altura_m = altura / 100  

            
            if sexo == "hombre":
                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
            else:
                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161


            flash(f"Tu TMB es: {tmb:.2f} kcal por día.", "success")

        except ValueError:
            flash("Verifica los datos ingresados.", "danger")

    return render_template("tmb.html")

@app.route("/gct", methods=["GET", "POST"])
def gct():
    resultado = None
    try:
        if request.method == "POST":
        
            edad = request.form.get("edad", "").strip()
            altura = request.form.get("altura", "").strip()
            peso = request.form.get("peso", "").strip()
            genero = request.form.get("genero", "").strip()
            actividad = request.form.get("actividad", "").strip()

            if not (edad and altura and peso and genero and actividad):
                flash("Por favor completa todos los campos.", "warning")
                return redirect(url_for("gct"))

            edad = float(edad)
            altura = float(altura)   
            peso = float(peso)


            multiplicador = {
                "sedentario": 1.2,
                "ligero": 1.375,
                "moderado": 1.55,
                "intenso": 1.725,
                "muy_intenso": 1.9
            }

            factor = multiplicador.get(actividad)
            if factor is None:
                flash("Selecciona un nivel de actividad válido.", "warning")
                return redirect(url_for("gct"))

            
            if genero == "hombre":
                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
            else:
                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

            gct_valor = tmb * factor

            
            resultado = {
                "tmb": round(tmb, 2),
                "gct": round(gct_valor, 2),
                "factor": factor
            }

            
            return render_template("gct.html", resultado=resultado)

    except ValueError:
        flash("Por favor ingresa valores numéricos válidos.", "danger")
        return redirect(url_for("gct"))
    except Exception as e:
        
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("gct"))

    
    return render_template("gct.html", resultado=resultado)

@app.route("/pci", methods=["GET", "POST"])
def pci():
    resultado = None

    if request.method == "POST":
        try:
            altura = float(request.form["altura"])
            genero = request.form["genero"]

            
            if genero == "hombre":
                pci_valor = 50 + 0.9 * (altura - 152)
            else:
                pci_valor = 45.5 + 0.9 * (altura - 152)

            resultado = f"Tu peso corporal ideal es: {pci_valor:.2f} kg"

        except:
            resultado = "Por favor ingresa valores válidos."

    return render_template("pci.html", resultado=resultado)


@app.route("/macros", methods=["GET", "POST"])
def macros():
    resultado = None
    proteinas = carbohidratos = grasas = None

    if request.method == "POST":
        try:
            peso = float(request.form["peso"])
            altura = float(request.form["altura"])
            edad = int(request.form["edad"])
            genero = request.form["genero"]
            objetivo = request.form["objetivo"]
            actividad = float(request.form["actividad"])
            dieta = request.form["dieta"]

            
            if genero == "hombre":
                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
            else:
                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

            
            gct = tmb * actividad

            
            if objetivo == "perder":
                calorias = gct - 500
            elif objetivo == "ganar":
                calorias = gct + 400
            else:
                calorias = gct

            
            if dieta == "balanceada":
                porc_p = 0.30
                porc_c = 0.45
                porc_g = 0.25

            elif dieta == "alta_proteina":
                porc_p = 0.40
                porc_c = 0.35
                porc_g = 0.25

            else:
                porc_p = 0.35
                porc_c = 0.20
                porc_g = 0.45

            
            proteinas = (calorias * porc_p) / 4
            carbohidratos = (calorias * porc_c) / 4
            grasas = (calorias * porc_g) / 9

            resultado = f"Calorías recomendadas: {calorias:.0f} kcal"

        except:
            flash("Por favor ingresa valores válidos.", "danger")

    return render_template("macros.html",
                    resultado=resultado,
                    proteinas=proteinas,
                    carbohidratos=carbohidratos,
                    grasas=grasas)


if __name__ == "__main__":
    app.run(debug=True)
