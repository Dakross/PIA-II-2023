from flask import Flask, render_template, request
import pandas as pd
from hola import juancarlosbodoque

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
            return render_template('about.html')

    return render_template('about.html',)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/juancarlosbodoque', methods=("POST", "GET"))
def juan():
    return juancarlosbodoque()

if __name__ == '__main__':
    app.run()
