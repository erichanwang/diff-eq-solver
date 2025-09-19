import sympy

def solve_homogeneous_ode(coeffs, initial_conditions):
    """
    Solves a homogeneous linear ordinary differential equation with constant coefficients.

    Args:
        coeffs (dict): A dictionary of coefficients for the derivatives of y.
                       Example: {'3': 1, '2': 2, '1': -3} for y''' + 2y'' - 3y' = 0
        initial_conditions (dict): A dictionary of initial conditions.
                                   Example: {0: 1, 1: 0, 2: 4} for y(0)=1, y'(0)=0, y''(0)=4

    Returns:
        str: The solution to the differential equation.
    """
    x = sympy.symbols('x')
    y = sympy.Function('y')(x)

    # Construct the differential equation
    diffeq = 0
    for order, coeff in coeffs.items():
        diffeq += coeff * sympy.diff(y, x, int(order))

    # Solve the general solution
    general_solution = sympy.dsolve(diffeq, y)

    # Apply initial conditions to find constants
    if initial_conditions:
        constants = sympy.solve([
            general_solution.rhs.subs(x, 0) - initial_conditions.get('0', 0),
            sympy.diff(general_solution.rhs, x).subs(x, 0) - initial_conditions.get('1', 0),
            sympy.diff(general_solution.rhs, x, 2).subs(x, 0) - initial_conditions.get('2', 0),
            sympy.diff(general_solution.rhs, x, 3).subs(x, 0) - initial_conditions.get('3', 0)
        ])
        if isinstance(constants, list):
            constants = constants[0]
        
        solution = general_solution.subs(constants)
    else:
        solution = general_solution

    return str(solution.rhs)

if __name__ == '__main__':
    # Example usage: y'' - y = 0, y(0)=1, y'(0)=0
    # The characteristic equation is r^2 - 1 = 0, so r = 1, -1.
    # y(x) = C1*exp(x) + C2*exp(-x)
    # y(0) = C1 + C2 = 1
    # y'(x) = C1*exp(x) - C2*exp(-x)
    # y'(0) = C1 - C2 = 0
    # Solving gives C1=1/2, C2=1/2.
    # y(x) = (exp(x) + exp(-x))/2 = cosh(x)
    
    coeffs_example = {'2': 1, '0': -1} # y'' - y = 0
    ics_example = {'0': 1, '1': 0} # y(0)=1, y'(0)=0
    solution_str = solve_homogeneous_ode(coeffs_example, ics_example)
    print(f"The solution is: y(x) = {solution_str}")
