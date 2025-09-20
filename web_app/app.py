from flask import Flask, render_template, request, jsonify
import sys
import os
import sympy

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
        if value:
            try:
                parsed_value = sympy.sympify(value)
                if key.startswith('coeff'):
                    order = key.replace('coeff', '')
                    coeffs[order] = parsed_value
                elif key.startswith('ic'):
                    order = key.replace('ic', '')
                    initial_conditions[order] = parsed_value
            except (sympy.SympifyError, TypeError):
                return jsonify({'error': f"Invalid mathematical expression: {value}"})

    solution_data = solve_homogeneous_ode(coeffs, initial_conditions)
    
    return jsonify(solution_data)

if __name__ == '__main__':
    app.run(debug=True)
