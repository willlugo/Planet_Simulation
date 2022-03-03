import pygame
import numpy as np


class Planet():
    AU = 149.6e9
    G = 6.67408e-11
    SCALE = float(250) / AU # 1AU = 100 pixels
    TIMESTEP = float(3600 * 24) # 1 day

    def __init__(self, x, y, radius, colour, mass):
        self.x = x
        self.y = y
        self.radius = radius # radius planet will be drawn in
        self.colour = colour
        self.mass = mass # mass of planet in kg

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.velx = 0
        self.vely = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + (WIDTH / 2)
        y = self.y * self.SCALE + (HEIGHT / 2)
        pygame.draw.circle(win, self.colour, (x, y), self.radius)
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - other.y
        distance = np.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = (self.G * self.mass * other.mass) / (distance**2)
        theta = np.arctan2(distance_y, distance_x)
        force_x = np.cos(theta) * force
        force_y = np.sin(theta) * force
        #force = (self.G * self.mass * other.mass) / (distance_xy**2)
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            force_x, force_y = self.attraction(planet)
            total_fx += force_x
            total_fy += force_y

        
        self.velx += total_fx / self.mass * self.TIMESTEP
        self.vely += total_fy / self.mass * self.TIMESTEP
        self.x += self.velx * self.TIMESTEP
        self.y += self.vely * self.TIMESTEP
        self.orbit.append((self.x, self.y))


pygame.init()
FPS = 60
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(float(0), float(0), 30, YELLOW, 1.9882 * 10**30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, float(0), 8, DARK_GREY, 3.30 * 10**23)
    mercury.vely = -47.4 * 1000
    venus = Planet(0.723 * Planet.AU, float(0), 14, WHITE, 4.8685 * 10**24)
    venus.vely = -35.02 * 1000
    earth = Planet(-1 * Planet.AU, float(0), 16, BLUE, 5.9742 * 10**24)
    earth.vely = 24.077 * 1000
    mars = Planet(-1.524 * Planet.AU, float(0), 12, RED, 6.39 * 10**23)
    mars.vely = 24.077 * 1000
    

    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(FPS)
        WIN.fill(BLACK)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update()

    pygame.quit()


main()