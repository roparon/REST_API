from flask import Flask, request

app = Flask(__name__)

# 1. Route with division by zero
@app.route('/divide')
def divide():
    num = int(request.args.get('num'))
    return str(100 / num)  # Try ?num=0 to trigger an error

# 2. Route with NoneType error
@app.route('/length')
def length():
    name = request.args.get('name')
    return f"Length: {len(name)}"  # Try without ?name= to trigger an error

# 3. Route with wrong type operation
@app.route('/add')
def add():
    a = request.args.get('a')  # No type conversion!
    b = request.args.get('b')
    return f"Sum: {a + b}"  # Try ?a=10&b=5 and see what happens

# 4. Route with undefined variable
@app.route('/undefined')
def undefined():
    return f"The value is: {value}"  # 'value' is not defined

# 5. Route with a bad index
@app.route('/index')
def index():
    data = [1, 2, 3]
    i = int(request.args.get('i'))
    return f"Item: {data[i]}"  # Try ?i=5 to get IndexError

# 6. Route expecting POST but called with GET
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form['data']  # KeyError if 'data' is missing
    return f"Received: {data}"

# 7. Route calling a missing function
@app.route('/call')
def call():
    return missing_function()  # Function is not defined

# 8. Route with a logic bug
@app.route('/check-age')
def check_age():
    age = int(request.args.get('age'))
    if age < 18:
        return "You are underage."
    elif age > 18:
        return "You are an adult."
    else:
        return "Age is unknown?"  # What if age == 18?

if __name__ == '__main__':
    app.run(debug=True)
