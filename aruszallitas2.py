import pulp
import time

fullstart = time.perf_counter()

model = pulp.LpProblem("Aruszallitas", pulp.LpMinimize)

forrasok = ["gy", "r"]
celok = list(range(1, 9))

koltseg = {
    "gy": {1: 14,   2: 25, 3: 21, 4: 20,   5: 21.5, 6: 19,   7: 17, 8: 30},
    "r":  {1: 24,   2: 15, 3: 28, 4: 20,   5: 18.5, 6: 19.5, 7: 24, 8: 28},
}

kapacitas = {"gy": 100, "r": 45}

igeny = {1: 22, 2: 14, 3: 18, 4: 17, 5: 15, 6: 13, 7: 15, 8: 20}

# 2D változó-mátrix: x[forrás][cél]
x = pulp.LpVariable.dicts("x", (forrasok, celok), lowBound=0, cat="Integer")

# Célfüggvény
model += pulp.lpSum(koltseg[f][c] * x[f][c] for f in forrasok for c in celok)

# Kapacitás korlátok (soronként)
for f in forrasok:
    model += pulp.lpSum(x[f][c] for c in celok) <= kapacitas[f]

# Igény korlátok (oszloponként)
for c in celok:
    model += pulp.lpSum(x[f][c] for f in forrasok) == igeny[c]

start = time.perf_counter()
model.solve()
end = time.perf_counter()
print(f"Model solve time {(end-start) * 1000}")

for f in forrasok:
    for c in celok:
        val = int(pulp.value(x[f][c]))
        if val > 0:
            print(f"x[{f}][{c}]: {val} db")


print(f"Total cost: {int(pulp.value(model.objective))} $")  # 2583

fullend = time.perf_counter()
print(f"Full solve time {(fullend-fullstart) * 1000}")
