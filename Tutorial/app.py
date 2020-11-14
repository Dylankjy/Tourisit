from flask import Flask, render_template, redirect, url_for, request
import math

app = Flask(__name__)


@app.route('/')
def ez():
    return render_template('in.html')


@app.route('/test')
def home():
    db = {'The Nightlife of Bishan':50, 'See the Nightlife of Bishan':50, 'See the lights at Orchard':50, 'See the Nature at Bay Area':50, 'See the whole of SG': 100}
    cols = math.ceil(len(db)/4)
    return render_template('index.html', db=db, no_cols=cols)


if __name__ == '__main__':
    app.run(debug=True)