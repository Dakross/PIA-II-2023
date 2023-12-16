from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
from hola import index
from flask_bootstrap import Bootstrap4

app = Flask(__name__)
bootstrap = Bootstrap4(app)

@app.route('/about', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
            return render_template('about.html')

    return render_template('about.html',)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/', methods=("POST", "GET"))
def indexado():
    return index()

@app.route('/toggle-theme')
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))

if __name__ == '__main__':
    app.run(debug=True)