import pulp
import pandas as pd


A = pd.DataFrame(
    {
        "name": ["cost", "gain"],
        "I":    [10.2,  8],
        "II":   [6,     3],
        "III":  [23,    15],
        "IV":   [11.1,  7],
        "V":    [9.8,   10],
        "VI":   [31.6,  12]
    }
).set_index("name")

# A feladat

"""
model = pulp.LpProblem("verseny", pulp.LpMaximize)

x1 = pulp.LpVariable("I", cat = "Binary")
x2 = pulp.LpVariable("II", cat = "Binary")
x3 = pulp.LpVariable("III", cat = "Binary")
x4 = pulp.LpVariable("IV", cat = "Binary")
x5 = pulp.LpVariable("V", cat = "Binary")
x6 = pulp.LpVariable("VI", cat = "Binary")

model += A.loc["gain", "I"] * x1 + A.loc["gain", "II"] * x2 + A.loc["gain", "III"] * x3 + A.loc["gain", "IV"] * x4 + A.loc["gain", "V"] * x5 + A.loc["gain", "VI"] * x6

model += A.loc["cost", "I"] * x1 + A.loc["cost", "II"] * x2 + A.loc["cost", "III"] * x3 + A.loc["cost", "IV"] * x4 + A.loc["cost", "V"] * x5 + A.loc["cost", "VI"] * x6 <= 35

model.solve()

for v in model.variables():
    print(f"{v.name}: {int(pulp.value(v))} db")
print(pulp.value(model.objective))
"""
# b feladat: minimum 30 km/h növekedés, minimális ráfordítással

model = pulp.LpProblem("verseny", pulp.LpMinimize)


x1 = pulp.LpVariable("I", cat = "Binary")
x2 = pulp.LpVariable("II", cat = "Binary")
x3 = pulp.LpVariable("III", cat = "Binary")
x4 = pulp.LpVariable("IV", cat = "Binary")
x5 = pulp.LpVariable("V", cat = "Binary")
x6 = pulp.LpVariable("VI", cat = "Binary")

model += A.loc["cost", "I"] * x1 + A.loc["cost", "II"] * x2 + A.loc["cost", "III"] * x3 + A.loc["cost", "IV"] * x4 + A.loc["cost", "V"] * x5 + A.loc["cost", "VI"] * x6

model += A.loc["gain", "I"] * x1 + A.loc["gain", "II"] * x2 + A.loc["gain", "III"] * x3 + A.loc["gain", "IV"] * x4 + A.loc["gain", "V"] * x5 + A.loc["gain", "VI"] * x6 >= 30

model.solve()

for v in model.variables():
    print(f"{v.name}: {int(pulp.value(v))} db")
print(f"Speed gained: {pulp.value(model.objective)}")
cost = 0
i = 0
for v in model.variables():
    cost += A.iloc[0, i] * int(pulp.value(v)) 
print(f"Cost: {int(round(cost,1)*1000)} $")