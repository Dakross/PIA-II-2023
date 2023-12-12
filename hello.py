from flask import Flask, render_template, request
import pandas as pd
from hola import index

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
            return render_template('about.html')

    return render_template('about.html',)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index', methods=("POST", "GET"))
def indexado():
    return index()

if __name__ == '__main__':
    app.run()
