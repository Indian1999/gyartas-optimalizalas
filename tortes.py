import pulp

model = pulp.LpProblem("mixedInteger", pulp.LpMinimize)

#cat = "Integer"
cat = "Continuous"
x1 = pulp.LpVariable("x1", lowBound = 0, cat = cat)
x2 = pulp.LpVariable("x2", lowBound = 0, cat = cat)

model += -3*x1 -4*x2 + 20
model += 2/5*x1 + x2 <= 3
model += 2/5*x1 - 2/5*x2 <= 1
model += x2 >= 2
model += x1 >= 3

model.solve()

print("2/5*x1 + x2 =",2/5*pulp.value(x1) + pulp.value(x2))
print("2/5*x1 - 2/5*x2 =",2/5*pulp.value(x1) - 2/5*pulp.value(x2))
print("-3*x1 -4*x2 + 20 =",-3*pulp.value(x1) -4*pulp.value(x2) + 20)
for v in model.variables():
    print(f"{v.name}: {float(pulp.value(v))}")

print(f"Total cost: {float(pulp.value(model.objective))}") 

"""
x1: 2.0
x2: 2.0
Total cost: 6.0

Ha folytonos:
x1: 3.9285714
x2: 1.4285714
Total cost: 2.500000199999999
"""