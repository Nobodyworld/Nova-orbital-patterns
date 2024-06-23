import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aether Simulation")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

# Aether particle class
class AetherParticle:
    def __init__(self, x, y, charge):
        self.x = x
        self.y = y
        self.charge = charge  # +1 for positive, -1 for negative
        self.vx = 0
        self.vy = 0

    def update_position(self):
        self.x += self.vx
        self.y += self.vy

    def apply_force(self, fx, fy):
        self.vx += fx
        self.vy += fy

    def draw(self):
        color = blue if self.charge > 0 else red
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 5)

# Create a list of aether particles
particles = [AetherParticle(random.randint(100, 700), random.randint(100, 500), random.choice([-1, 1])) for _ in range(20)]

# Function to calculate forces based on displacement vectors
def calculate_forces():
    for i, particle in enumerate(particles):
        fx, fy = 0, 0
        for j, other in enumerate(particles):
            if i != j:
                dx = other.x - particle.x
                dy = other.y - particle.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > 0:
                    # Apply an inverse square law force
                    force = (particle.charge * other.charge) / distance**2
                    fx += force * dx / distance
                    fy += force * dy / distance
        particle.apply_force(fx, fy)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate forces and update particle positions
    calculate_forces()
    for particle in particles:
        particle.update_position()
        particle.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
