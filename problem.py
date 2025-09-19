# y''' - 2y'' - y' + 2y = 0
# y(0) = 4, y'(0) = 6, y''(0) = 10

from sympy import symbols, Function, Eq, dsolve

t = symbols('t')
y = Function('y')

# Define ODE
ode = Eq(y(t).diff(t,3) - 2*y(t).diff(t,2) - y(t).diff(t) + 2*y(t), 0)

# Solve with initial conditions
sol = dsolve(ode, ics={y(0): 4, y(t).diff(t).subs(t,0): 6, y(t).diff(t,2).subs(t,0): 10})
sol
