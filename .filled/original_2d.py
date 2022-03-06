from graphics import *
import logging
import random
from itertools import product
import math
from colorsys import hsv_to_rgb


#################################################################
#  VECTOR OPERATIONS                                            #
#################################################################


# Gets the distance between two vectors
def dist(p1, p2):
    p1x = p1.getX()
    p1y = p1.getY()
    p2x = p2.getX()
    p2y = p2.getY()
    dx = (p1x - p2x) ** 2
    dy = (p1y - p2y) ** 2
    return math.sqrt(dx + dy)


# Takes the dot product of two vectors
def dot_prod(p1, p2):
    term1 = p1.getX() * p2.getX()
    term2 = p1.getY() * p2.getY()
    return term1 + term2


# Projects vector p1 onto vector p2
def proj(p1, p2):
    numer = dot_prod(p1, p2)
    denom = dot_prod(p2, p2)
    scalar = numer / denom
    new_x = scalar * p2.getX()
    new_y = scalar * p2.getY()
    return Point(new_x, new_y)


# Adds two vectors
def vec_add(p1, p2):
    new_x = p1.getX() + p2.getX()
    new_y = p1.getY() + p2.getY()
    return Point(new_x, new_y)


# Subtracts vector p2 from p1
def vec_sub(p1, p2):
    new_x = p1.getX() - p2.getX()
    new_y = p1.getY() - p2.getY()
    return Point(new_x, new_y)


# Multiplies a vector p by a scalar s
def vec_scale(p, s):
    return Point(s * p.getX(), s * p.getY())


#################################################################
#  USEFUL FUNCTIONS                                             #
#################################################################


# Return true if circle Ci overlaps with circle Cj
def circles_overlap(Ci, Cj):
    return dist(Ci.getCenter(), Cj.getCenter()) <= Ci.getRadius() + Cj.getRadius()


# Return true if circle Ci DOESN'T overlap with ANY circles from the list
def valid_placement(Ci, C_list):
    for Cj in C_list:
        if circles_overlap(Ci, Cj):
            return False
    return True


# Gets a random color using HSV (prettier than usiong RGB)
def rand_color():
    h = random.uniform(0, 1)
    s = random.uniform(0.4, 1)
    r,g,b = hsv_to_rgb(h, s, 1)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return color_rgb(r, g, b)


# Given two balls Ci and Cj it will bounce
# NOTE: This is only realistic if all balls have the same mass!
# NOTE: This doesn't check if the balls have actually collided!
def bounce_ball(Ci, vi, Cj, vj):
    Oi = Ci.getCenter()
    Oj = Cj.getCenter()

    delta_i = proj(vec_sub(vi,vj), vec_sub(Oi,Oj))
    delta_j = vec_scale(delta_i, -1)

    new_vi = vec_sub(vi, delta_i)
    new_vj = vec_sub(vj, delta_j)

    return new_vi, new_vj


#################################################################
#  SETUP CODE                                                   #
#################################################################


# Create the window
WIN_W, WIN_H = 600, 600
win = GraphWin('Bouncing Balls', WIN_W, WIN_H, autoflush=False)
win.setBackground('white')

# How many circles?
NUM_CIRCLES = 30

# Initial list of circles and their velocities is empty, will
# generate them next
circles = [None] * NUM_CIRCLES
vels = [None] * NUM_CIRCLES

# Create each circle one at a time
for i in range(NUM_CIRCLES):
    # STEP 1. How big is each circle?

    # All circles have the same radius for now
    R = 20

    # STEP 2. Where should the circle be placed?

    # Keep trying to place the latest circle, re-trying if it turns
    # out that it overlaps with a previous one
    while True:
        x = random.randint(R, WIN_W - R)
        y = random.randint(R, WIN_H - R)
        circles[i] = Circle(Point(x,y), R)
        if valid_placement(circles[i], circles[:i]):
            break

    # STEP 3. How fast should the circle move initially?

    # All balls start with the same momentum
    rho = 1600

    # Assume mass is directly proportional to area (drop the constants)
    m = R ** 2

    # Solve for velocity
    v = rho / m

    # The direction of the velocity is chosen at random
    theta = random.uniform(0, 2*math.pi)
    vx = v * math.cos(theta)
    vy = v * math.sin(theta)
    vels[i] = Point(vx,vy)

    # STEP 4. How should the circles look?

    # Give the circles a border, a random fill color, and then
    # draw them on the screen
    circles[i].setWidth(3)
    circles[i].setFill(rand_color())

    # STEP 5. Draw the circle on the screen

    circles[i].draw(win)

# The following properties are needed for collision detection to not be glitchy:

# This is true if a circle has already bounced off the left or right wall
bounced_x = [False for i in range(NUM_CIRCLES)]

# This is true if a circle has already bounced off the top or bottom wall
bounced_y = [False for i in range(NUM_CIRCLES)]

# This is true if a circle i has already bounced off circle j
collided = [[False for i in range(NUM_CIRCLES)] for j in range(NUM_CIRCLES)]


#################################################################
#  MAIN LOOP!                                                   #
#################################################################


while True:
    # Move each circle based on its velocity
    for i in range(NUM_CIRCLES):
        vx = vels[i].getX()
        vy = vels[i].getY()
        circles[i].move(vx, vy)

    # Ball/wall collision detection
    for i in range(NUM_CIRCLES):
        O = circles[i].getCenter()
        Ox = O.getX()
        Oy = O.getY()
        R = circles[i].getRadius()

        vx_new = vels[i].getX()
        vy_new = vels[i].getY()

        # Check for collision between ball and right/left wall
        if Ox + R > WIN_W:
            vx_new *= -1
            circles[i].move(WIN_W - Ox - R, 0)
            bounced_x[i] = True
        elif Ox - R < 0:
            vx_new *= -1
            circles[i].move(R - Ox, 0)
            bounced_x[i] = True
        else:
            bounced_x[i] = False

        # Check for collision between ball and bottom/top wall
        if Oy + R > WIN_H:
            vy_new *= -1
            circles[i].move(0, WIN_H - Oy - R)
            bounced_y[i] = True
        elif Oy - R < 0:
            vy_new *= -1
            circles[i].move(0, R - Oy)
            bounced_y[i] = True
        else:
            bounced_y[i] = False

        vels[i] = Point(vx_new, vy_new)

    # Ball/ball collision detection
    for i in range(NUM_CIRCLES):
        for j in range(i+1, NUM_CIRCLES):
            if i == j:
                continue
            Ci = circles[i]
            vi = vels[i]
            Cj = circles[j]
            vj = vels[j]
            if circles_overlap(Ci, Cj):
                if not collided[i][j]:
                    collided[i][j] = True
                    new_vi, new_vj = bounce_ball(Ci, vi, Cj, vj)
                    vels[i] = new_vi
                    vels[j] = new_vj
            else:
                collided[i][j] = False

    # Run the program at 120 FPS
    update(120)

    # If the window is closed, exit the program
    if win.isClosed():
        exit()
