from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the parent directory to the path to import the solver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from solver import solve_homogeneous_ode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    
    coeffs = {}
    initial_conditions = {}

    for key, value in data.items():
        if key.startswith('coeff'):
            order = key.replace('coeff', '')
            coeffs[order] = int(value)
        elif key.startswith('ic'):
            order = key.replace('ic', '')
            initial_conditions[order] = int(value)

    solution = solve_homogeneous_ode(coeffs, initial_conditions)
    
    return jsonify({'solution': solution})

if __name__ == '__main__':
    app.run(debug=True)
