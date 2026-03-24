# PSO (Particle Swarm Optimization) [Részecske Raj Optimalizáció]
import numpy as np # pip install numpy

variables = 5

# A részecske raj paraméterei
n_particles = 50
max_iter = 1000
w = 0.9 # inercia súly
c1 = 4 # Gyorsulási eggyütható
c2 = 4 # Gyorsulási eggyütható

# Részecskék létrehozása
# 1 részecske - a 6 különböző termékből, hány darabot gyártsunk (számhatos)
# 1 részecske sebesség 6 számmal írható le (vektor6)
particles = np.random.randint(0, 20, size = (n_particles, variables))
particles[:,3:] = np.random.randint(0,2, size = (n_particles, 2))
velocities = np.zeros((n_particles, variables)) # 50*6 os mátrix tele 0-kal

# Legjobb pozíciók inicializálása
pbest = np.copy(particles)
pbest_scores = np.array([-np.inf] * n_particles)
gbest = particles[0]
gbest_score = -np.inf

def evaluate(particle):
    if particle[0] < 0 or particle[1] < 0 or particle[2] < 0:
        return -np.inf
    if particle[3] != 0 or particle[3] != 0:
        return -np.inf
    if particle[4] != 0 or particle[4] != 0:
        return -np.inf
    if particle[0] + particle[1] > 120 * particle[3]:
        return -np.inf
    if particle[2] > 48 * particle[4]:
        return -np.inf
    if 10*particle[0] + 15 * particle[1] + 20 * particle[2] > 2000:
        return -np.inf
    return particle[0] * 410 + particle[1] * 520 + particle[2]*686 - 32*particle[0] - 32*particle[1] - 38.5*particle[2] - 2016*particle[3] - 1200*particle[4]

for _ in range(max_iter):
    for i in range(len(particles)):
        score = evaluate(particles[i])
        if score > pbest_scores[i]:
            pbest_scores[i] = score
            pbest[i] = particles[i]
        if score > gbest_score:
            gbest_score = score
            gbest = particles[i]

        velocities[i] = w * velocities[i] + c1 * np.random.rand() * (pbest[i] - particles[i]) + c2 * np.random.rand() * (gbest - particles[i])
        velocities = velocities.round().astype("int32")

        particles[i] += velocities[i]
        
        
print("Az optimális gyártási mennyiségek (legjobb pozíció csoport szinten):", gbest)
print("Maximális bevétel:", gbest_score)
        

    