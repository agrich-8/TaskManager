from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/register/<name>')
def register(name):
    return f'1111111{name}'
    
app.run(debug=True)
