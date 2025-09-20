import sympy

def solve_homogeneous_ode(coeffs, initial_conditions):
    """
    Solves a homogeneous linear ordinary differential equation with constant coefficients.

    Args:
        coeffs (dict): A dictionary of coefficients for the derivatives of y with respect to t.
                       Example: {'3': 1, '2': -2, '1': -1, '0': 2} for y'''(t) - 2y''(t) - y'(t) + 2y(t) = 0
        initial_conditions (dict): A dictionary of initial conditions.
                                   Example: {'0': 4, '1': 6, '2': 10} for y(0)=4, y'(0)=6, y''(0)=10

    Returns:
        dict: A dictionary containing the solution in both 'latex' and 'plain' formats, or an 'error' key.
    """
    t = sympy.symbols('t')
    y = sympy.Function('y')(t)

    # Construct the differential equation
    diffeq = 0
    for order, coeff in coeffs.items():
        diffeq += coeff * sympy.diff(y, t, int(order))

    equation = sympy.Eq(diffeq, 0)

    # Construct the initial conditions dictionary for dsolve
    ics = {}
    if initial_conditions:
        for order_str, value in initial_conditions.items():
            order = int(order_str)
            if order == 0:
                ics[y.subs(t, 0)] = value
            else:
                ics[sympy.diff(y, t, order).subs(t, 0)] = value

    # Solve the differential equation
    try:
        if ics:
            solution = sympy.dsolve(equation, y, ics=ics)
        else:
            solution = sympy.dsolve(equation, y)

        # Prepare both LaTeX and plain string solutions
        latex_solution = sympy.latex(solution.rhs)
        plain_solution = str(solution.rhs)

        return {'latex': latex_solution, 'plain': plain_solution}
    except Exception as e:
        return {'error': f"An error occurred while solving: {e}"}

if __name__ == '__main__':
    # Example: y'''(t) - 2y''(t) - y'(t) + 2y(t) = 0
    # y(0) = 4, y'(0) = 6, y''(0) = 10
    coeffs_example = {'3': 1, '2': -2, '1': -1, '0': 2}
    ics_example = {'0': 4, '1': 6, '2': 10}
    solution = solve_homogeneous_ode(coeffs_example, ics_example)
    print(f"The solution is: {solution}")
