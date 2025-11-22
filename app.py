from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "clavexdffdd"

USUARIOS_REGISTRADOS = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bienvenida")
def bienvenida():
    return render_template("bienvenida.html")






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
        peso = request.form.get("peso", "").replace(",", ".")
        altura = request.form.get("altura", "").replace(",", ".")
        edad = request.form.get("edad", "").strip()
        sexo = request.form.get("sexo", "").strip().lower()

        
        if not peso or not altura or not edad or sexo not in ["masculino", "femenino"]:
            return render_template("imc.html", error="Por favor llena todos los campos correctamente")

        try:
            peso = float(peso)
            altura = float(altura) / 100 
            edad = int(edad)
        except ValueError:
            return render_template("imc.html", error="Introduce números válidos para peso, altura y edad")

        if altura == 0:
            return render_template("imc.html", error="La altura no puede ser cero")

        imc = peso / (altura * altura)
        imc = round(imc, 2)  

        
        if edad >= 18:  
            if imc < 18.5:
                resultado = {"estado": "Bajo peso", "imagen": "bajo2.png"}
                mensaje = "Necesitas mejorar tu alimentación."
            elif imc < 25:
                resultado = {"estado": "Normal", "imagen": "normal2.png"}
                mensaje = "¡Estás en un buen rango, sigue así!"
            elif imc < 30:
                resultado = {"estado": "Sobrepeso", "imagen": "sobrepeso2.png"}
                mensaje = "Cuida un poco más tus hábitos."
            else:
                resultado = {"estado": "Obesidad", "imagen": "obeso2.png"}
                mensaje = "Toma acción para mejorar tu salud."
        else:  
            resultado = {"estado": "Menor de 18 años", "imagen": "infantil.png"}
            mensaje = f"Tu IMC es {imc}. Para niños y adolescentes, consulta con un especialista para interpretar correctamente el IMC según edad y sexo."

        return render_template("imc.html", resultado=resultado, imc=imc)

    return render_template("imc.html")






@app.route("/tmb", methods=["GET", "POST"])
def tmb():
    if request.method == "POST":
        sexo = request.form.get("sexo")
        peso = request.form.get("peso", "").replace(",", ".")
        altura = request.form.get("altura", "").replace(",", ".")
        edad = request.form.get("edad", "").replace(",", ".")

        if not sexo or not peso.strip() or not altura.strip() or not edad.strip():
            return render_template("tmb.html", error="Por favor, llena todos los campos")

        try:
            peso = float(peso)
            altura = float(altura)
            edad = float(edad)
        except ValueError:
            return render_template("tmb.html", error="Introduce valores numéricos válidos")


        if sexo == "hombre":
            tmb_resultado = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
        else:
            tmb_resultado = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

        tmb_final = round(tmb_resultado, 2)

        return render_template("tmb.html", resultado=tmb_final)

    return render_template("tmb.html")





@app.route("/gct", methods=["GET", "POST"])
def gct():
    if request.method == "POST":
        try:
            peso = float(request.form["peso"])
            altura = float(request.form["altura"])
            edad = int(request.form["edad"])
            sexo = request.form["sexo"]
            actividad = float(request.form["actividad"])

            
            if sexo == "h":
                geb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
            else:
                geb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

            
            gct_total = round(geb * actividad)

            return render_template("gct.html", resultado=gct_total)

        except:
            return render_template("gct.html", resultado="Error en los datos")

    return render_template("gct.html")


@app.route("/pci", methods=["GET", "POST"])
def pci():
    if request.method == "POST":
        try:
            altura = float(request.form["altura"])
            sexo = request.form["sexo"]

            
            altura_m = altura / 100

            
            if sexo == "h":
                pci = 50 + 2.3 * ((altura_m * 100 / 2.54) - 60)
            else:
                pci = 45.5 + 2.3 * ((altura_m * 100 / 2.54) - 60)

            pci = round(pci, 1)

            return render_template("pci.html", resultado=pci)

        except:
            return render_template("pci.html", resultado="Error al procesar los datos")

    return render_template("pci.html")



@app.route("/macronutrientes", methods=["GET", "POST"])
def macros():
    resultado = None

    if request.method == "POST":
        try:
            sexo = request.form.get("sexo")
            edad = float(request.form.get("edad"))
            peso = float(request.form.get("peso"))
            altura = float(request.form.get("altura"))
            actividad = request.form.get("actividad")


            if sexo == "hombre":
                tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
            else:
                tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)


            factores = {
                "sedentario": 1.2,
                "ligero": 1.375,
                "moderado": 1.55,
                "intenso": 1.725,
                "muy_intenso": 1.9
            }

            gct = tmb * factores[actividad]


            proteinas_g = peso * 2 
            proteinas_cal = proteinas_g * 4

            grasas_cal = gct * 0.30  
            grasas_g = grasas_cal / 9

            carbo_cal = gct - (proteinas_cal + grasas_cal)
            carbo_g = carbo_cal / 4

            resultado = {
                "tmb": round(tmb),
                "gct": round(gct),
                "proteinas": round(proteinas_g),
                "grasas": round(grasas_g),
                "carbohidratos": round(carbo_g),
            }

        except:
            resultado = "error"

    return render_template("macros.html", resultado=resultado)


@app.route("/recetas")
def recetas():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    return render_template("recetas.html")





if __name__ == "__main__":
    app.run(debug=True)
