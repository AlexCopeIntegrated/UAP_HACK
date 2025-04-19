from flask import Flask, jsonify
from random import randint, randrange
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route('/data')
def get_data():
    # Simulate your live data here
    data = [randrange(100) for _ in range(randint(20, 50))]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
