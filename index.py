import json

from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'hard to guess string'

todos = []

def guid():
    index = [0]
    def increase():
        index[0] = index[0] + 1
        return index[0]
    return increase

def find_index(todos, id):
    for i, v in enumerate(todos):
        if v['id'] == int(id):
            return i
    pass;

counter = guid()

@app.errorhandler(404)
def e404(e):
    return render_template('404.html')

@app.route('/')
def index():
    return render_template('index.html', todos = todos)

@app.route('/remove/<int:id>')
def remove_todo(id):
    index = find_index(todos, id)
    if isinstance(index, int):
        todos.pop(index)
        return '{"todoid":%d}' % id

@app.route('/add', methods=['POST'])
def add_todo():
    todo = None
    content = None
    content = request.form['content']
    todo = {
        'id' : counter(),
        'content' : content,
        'checked' : False
    }
    todos.append(todo)
    return json.dumps(todo)

@app.route('/check/<id>')
def check_todo(id):
    index = find_index(todos, id)
    if isinstance(index, int):
        todos[index]['checked'] = not todos[index]['checked']
        if todos[index]['checked']:
            return '{"checked":true}'
        else:
            return '{"checked":false}'

if __name__ == '__main__':
    app.run()