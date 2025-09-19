import sympy

def solve_homogeneous_ode(coeffs, initial_conditions):
    """
    Solves a homogeneous linear ordinary differential equation with constant coefficients.

    Args:
        coeffs (dict): A dictionary of coefficients for the derivatives of y.
                       Example: {'3': 1, '2': -2, '1': -1, '0': 2} for y''' - 2y'' - y' + 2y = 0
        initial_conditions (dict): A dictionary of initial conditions.
                                   Example: {'0': 4, '1': 6, '2': 10} for y(0)=4, y'(0)=6, y''(0)=10

    Returns:
        str: The solution to the differential equation.
    """
    x = sympy.symbols('x')
    y = sympy.Function('y')(x)

    # Construct the differential equation
    diffeq = 0
    for order, coeff in coeffs.items():
        diffeq += coeff * sympy.diff(y, x, int(order))

    equation = sympy.Eq(diffeq, 0)

    # Construct the initial conditions dictionary for dsolve
    ics = {}
    if initial_conditions:
        for order_str, value in initial_conditions.items():
            order = int(order_str)
            if order == 0:
                ics[y.subs(x, 0)] = value
            else:
                ics[sympy.diff(y, x, order).subs(x, 0)] = value
    
    # Solve the differential equation
    try:
        if ics:
            solution = sympy.dsolve(equation, y, ics=ics)
        else:
            solution = sympy.dsolve(equation, y)

        if solution:
            return str(solution.rhs)
        else:
            return "Could not find a solution."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    # Example from problem.py: y''' - 2y'' - y' + 2y = 0
    # y(0) = 4, y'(0) = 6, y''(0) = 10
    coeffs_example = {'3': 1, '2': -2, '1': -1, '0': 2}
    ics_example = {'0': 4, '1': 6, '2': 10}
    solution_str = solve_homogeneous_ode(coeffs_example, ics_example)
    print(f"The solution is: y(x) = {solution_str}")
    # Expected: 3*exp(t) + 2*exp(2*t) - exp(-t)
