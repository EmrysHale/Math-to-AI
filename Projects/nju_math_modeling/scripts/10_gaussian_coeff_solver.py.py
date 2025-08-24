import sympy as sp

a, b = sp.symbols('a b')
eq1 = b - a - 135.64
eq2 = b - a * sp.exp(7)

c,d=sp.symbols('c d')
eq3=d-c-1835.00
eq4=d-c*sp.exp(5)

solution1 = sp.solve((eq1, eq2), (a, b))
solution2=sp.solve((eq3,eq4),(c,d))

print(solution1)
print(solution2)

expr1 = b - a *sp.exp(6)
result1 = expr1.subs(solution1)
print(result1.evalf())

expr2 = d - c *sp.exp(4)
result2 = expr2.subs(solution2)
print(result2.evalf())