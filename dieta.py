"""
brownie;csokifagyi;cola;sajttorta
50;20;30;80
400;200;150;500
3;2;0;0
2;2;4;4
2;4;1;5

kell:
500 kalória, 6 dkg csoki, 10 dkg cukor, 8 dkg zsír
"""

import pulp
import os

path = "dieta.txt"

with open(path, "r", encoding = "utf-8") as f:
    next(f)

    prices = [int(item) for item in f.readline().split(";")]
    kcals = [int(item) for item in f.readline().split(";")]
    chocolate = [int(item) for item in f.readline().split(";")]
    sugars = [int(item) for item in f.readline().split(";")]
    fats = [int(item) for item in f.readline().split(";")]

model = pulp.LpProblem("Dieta", pulp.LpMinimize)

x1 = pulp.LpVariable("Brownie", lowBound = 0, cat = "Integer")
x2 = pulp.LpVariable("Csokifagyi", lowBound = 0, cat = "Integer")
x3 = pulp.LpVariable("Cola", lowBound = 0, cat = "Integer")
x4 = pulp.LpVariable("Sajttorta", lowBound = 0, cat = "Integer")

model += x1 * prices[0] + x2 * prices[1] + x3 * prices[2] + x4 * prices[3]
model += x1 * kcals[0] + x2 * kcals[1] + x3 * kcals[2] + x4 * kcals[3] >= 500
model += x1 * chocolate[0] + x2 * chocolate[1] + x3 * chocolate[2] + x4 * chocolate[3] >= 6
model += x1 * sugars[0] + x2 * sugars[1] + x3 * sugars[2] + x4 * sugars[3] >= 10
model += x1 * fats[0] + x2 * fats[1] + x3 * fats[2] + x4 * fats[3] >= 8

model.solve()


print(f"Brownie: {int(pulp.value(x1))} db")
print(f"Csokifagyi: {int(pulp.value(x2))} db")
print(f"Cola: {int(pulp.value(x3))} db")
print(f"Sajttorta: {int(pulp.value(x4))} db")
print(f"Költség: {int(pulp.value(model.objective))} Ft")