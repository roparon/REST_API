from flask import Flask, request

app = Flask(__name__)


@app.route('/divide')
def divide():
    num = int(request.args.get('num'))
    return str(100 / num)  


@app.route('/length')
def length():
    name = request.args.get('name')
    return f"Length: {len(name)}"  


@app.route('/add')
def add():
    a = request.args.get('a')  
    b = request.args.get('b')
    return f"Sum: {a + b}"  


@app.route('/undefined')
def undefined():
    return f"The value is: {value}"  


@app.route('/index')
def index():
    data = [1, 2, 3]
    i = int(request.args.get('i'))
    return f"Item: {data[i]}" 


@app.route('/submit', methods=['POST'])
def submit():
    data = request.form['data']  
    return f"Received: {data}"


@app.route('/call')
def call():
    return missing_function()  


@app.route('/check-age')
def check_age():
    age = int(request.args.get('age'))
    if age < 18:
        return "You are underage."
    elif age > 18:
        return "You are an adult."
    else:
        return "Age is unknown?"  

if __name__ == '__main__':
    app.run(debug=True)
