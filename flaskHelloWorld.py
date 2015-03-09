from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = False

@app.route('/')
def hello_world():
    return 'todo: epic webgl space game MMORPG with procedural everything and opencl multithreading!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
