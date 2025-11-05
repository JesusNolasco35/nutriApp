from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'c321234312312'  



@app.route('/')
def index():
     return render_template('index.html')

@app.route('/login')
def login():
     return render_template('login.html')

@app.route('/registro')
def registro():
     return render_template('registro.html')

@app.route('/logout')
def logout():
     session.clear()
     flash('Has cerrado sesión correctamente.', 'info')
     return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)