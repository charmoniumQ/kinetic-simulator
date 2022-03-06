import graphics

window = graphics.GraphWin(
    title='Bouncing Balls',
    width=600,
    height=800,
    autoflush=False,
)
window.setBackground('white')

n_objects = 2
masses = [3, 4]
positions = [100, 300]
velocities = [100, -60]
radiuses = [5, 10]
dt = 1/120

position_histories = []
objects = []
for i in range(n_objects):
    objects.append(graphics.Circle(0, 0, radiuses[i]))
    objects[i].draw(window)
    objects[i].setFill(graphics.rand_color())
    position_histories.append([])

clock = 0
clock_history = []
while window.isOpen() and clock < 2:
    clock_history.append(clock)
    for i in range(n_objects):
        positions[i] = positions[i] + dt * velocities[i]
        objects[i].set_pos(positions[i], 100)
        position_histories[i].append(positions[i])

    for i in range(n_objects):
        for j in range(n_objects):
            if i != j:
                if abs(positions[i] - positions[j]) < radiuses[i] + radiuses[j]:
                    combined_velocity = (velocities[i] * masses[i] + velocities[j] * masses[j]) / (masses[i] + masses[j])
                    velocities[i] = combined_velocity
    graphics.update(1/dt)
    clock += dt

import matplotlib.pyplot as plt
plt.plot(clock_history, position_histories[0])
plt.plot(clock_history, position_histories[1])
plt.xlabel("Time")
plt.ylabel("Distance")
plt.show()
