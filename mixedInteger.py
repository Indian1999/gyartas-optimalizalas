import pulp

model = pulp.LpProblem("mixedInteger", pulp.LpMaximize)

alfa = pulp.LpVariable("alfa", lowBound = 0, cat = "Integer")
beta = pulp.LpVariable("beta", lowBound = 0, cat = "Integer")
gamma = pulp.LpVariable("gamma", lowBound = 0, cat = "Integer")

fa = pulp.LpVariable("Fa", cat="Binary")
fc = pulp.LpVariable("Fc", cat="Binary")

model +=  alfa*410 + beta*520 + gamma*686 - 2016*fa - 1200*fc - 32 * alfa - 32*beta - 38.5*gamma
model += alfa + beta <= 120 * fa
model += gamma <= 48 * fc
model += 10*alfa + 15 * beta + 20 * gamma <= 2000

model.solve()

for v in model.variables():
    print(f"{v.name}: {int(pulp.value(v))} db")

print(f"Total cost: {float(pulp.value(model.objective))} $") 

"""
Fa: 1 db
Fc: 1 db
alfa: 120 db
beta: 0 db
gamma: 40 db
Total cost: 67804.0 $
"""