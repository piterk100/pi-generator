import pygame
import sys
from pygame.math import Vector2
from pygame.locals import *
import os, sys, math, pygame, pygame.mixer

licznik = 0

# Colors
black = 0, 0, 0
white = 255, 255, 255

# Screen size
screen_size = screen_width, screen_height = 600, 400

class MyRectangle:

    def __init__(self, position, mass, size, color = (255, 255, 255), velocity = pygame.math.Vector2(0, 0), width=1):
        self.position = position
        self.size = size
        self.color = color
        self.width = width
        self.velocity = velocity
        self.mass = mass

    def display(self):
        # Base rectangle
        points = [Vector2(0, self.size), Vector2(0, 0), Vector2(self.size, 0), Vector2(self.size, self.size)]
        # Fix y axis
        points = [Vector2(p.x, p.y * -1) for p in points]
        # Add current position
        points = [self.position + p * 2 for p in points]
        # Draw rectangle
        pygame.draw.polygon(screen, (255, 255, 255), points)


    def move(self):
        self.position.x += self.velocity * dtime
        self.bounce()

    def change_velocity(self, velocity):
        self.velocity = velocity

    def bounce(self):
        if self.position.x <= 0:
            global licznik
            licznik += 1
            self.velocity = self.velocity * (-1)
            print(licznik)

    def surface_distance(self, other, time):
        posB = self.position.x + self.velocity * time
        posL = other.position.x + other.velocity * time
        posBL = abs(posB - posL)
        sumBL = other.size + self.size
        return sumBL - posBL - 40

    def collide(self, other):
        if self.surface_distance(other, dtime) >= 0:
            global licznik
            licznik += 1
            vp1 = other.velocity
            vp2 = self.velocity
            self.velocity = (2*other.mass*vp1+vp2*(self.mass-other.mass))/(self.mass+other.mass)
            other.velocity = (other.mass*vp1+self.mass*(vp2-self.velocity))/other.mass
            print(licznik)

# Setting the display and getting the Surface object
screen = pygame.display.set_mode(screen_size)
# Getting the Clock object
clock = pygame.time.Clock()
# Setting a title to the windoww
pygame.display.set_caption("Pi")

sizeB = 50
xB = 400
yB = screen_height
color = white
velocityB = -100.0
mB = 100
rectangleB = MyRectangle(pygame.math.Vector2(xB, yB), mB, sizeB, color, velocityB)

sizeL = 10
xL = 200
yL = screen_height
color = white
velocityL = 0.0
mL = 1
rectangleL = MyRectangle(pygame.math.Vector2(xL, yL), mL, sizeL, color, velocityL)

# Defining variables for fps and continued running
fps_limit = 60
run_me = True
while run_me:
    # Limit the framerate
    dtime_ms = clock.tick(fps_limit)
    dtime = dtime_ms/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_me = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run_me = False

    # Clear the screen
    screen.lock()
    screen.fill(black)

    rectangleB.display()
    rectangleB.move()
    rectangleB.collide(rectangleL)

    rectangleL.display()
    rectangleL.move()
    #rectangleL.collide(rectangleB)

    screen.unlock()

    # Display everything in the screen
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
