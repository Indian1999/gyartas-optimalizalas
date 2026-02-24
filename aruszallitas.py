import pulp

model = pulp.LpProblem("Aruszallitas", pulp.LpMinimize)

xgy1 = pulp.LpVariable("gy1", lowBound = 0, cat = "Integer")
xgy2 = pulp.LpVariable("gy2", lowBound = 0, cat = "Integer")
xgy3 = pulp.LpVariable("gy3", lowBound = 0, cat = "Integer")
xgy4 = pulp.LpVariable("gy4", lowBound = 0, cat = "Integer")
xgy5 = pulp.LpVariable("gy5", lowBound = 0, cat = "Integer")
xgy6 = pulp.LpVariable("gy6", lowBound = 0, cat = "Integer")
xgy7 = pulp.LpVariable("gy7", lowBound = 0, cat = "Integer")
xgy8 = pulp.LpVariable("gy8", lowBound = 0, cat = "Integer")

xr1 = pulp.LpVariable("r1", lowBound = 0, cat = "Integer")
xr2 = pulp.LpVariable("r2", lowBound = 0, cat = "Integer")
xr3 = pulp.LpVariable("r3", lowBound = 0, cat = "Integer")
xr4 = pulp.LpVariable("r4", lowBound = 0, cat = "Integer")
xr5 = pulp.LpVariable("r5", lowBound = 0, cat = "Integer")
xr6 = pulp.LpVariable("r6", lowBound = 0, cat = "Integer")
xr7 = pulp.LpVariable("r7", lowBound = 0, cat = "Integer")
xr8 = pulp.LpVariable("r8", lowBound = 0, cat = "Integer")

model += 14*xgy1 + 25*xgy2 + 21*xgy3 + 20 * xgy4 + 21.5*xgy5 + 19*xgy6 + 17*xgy7 + 30*xgy8 + 24*xr1 + 15*xr2 + 28*xr3 + 20*xr4 + 18.5*xr5 + 19.5*xr6 + 24*xr7 + 28*xr8
model += xr1 + xr2 + xr3 + xr4 + xr5 + xr6 + xr7 + xr8 <= 45
model += xgy1 + xgy2 + xgy3 + xgy4 + xgy5 + xgy6 + xgy7 + xgy8 <= 100
model += xgy1 + xr1 == 22
model += xgy2 + xr2 == 14
model += xgy3 + xr3 == 18
model += xgy4 + xr4 == 17
model += xgy5 + xr5 == 15
model += xgy6 + xr6 == 13
model += xgy7 + xr7 == 15
model += xgy8 + xr8 == 20

model.solve()

for v in model.variables():
    print(f"{v.name}: {int(pulp.value(v))} db")


print(f"Total cost: {float(pulp.value(model.objective))} $") # 2583.5