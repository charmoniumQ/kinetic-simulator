import graphics

window = graphics.GraphWin(
    title='Bouncing Balls',
    width=800,
    height=600,
    autoflush=False,
)
window.setBackground('white')

dt = 1/120
radius = 10
particle = graphics.Circle(0, 0, radius)

particle.draw(window)
particle.setFill(graphics.rand_color())

while window.isOpen():
    particle.set_pos(300, 300)
    graphics.update(1/dt)
