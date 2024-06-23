import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Luminiferous Aether Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Particle parameters
particle_radius = 5
num_particles = 50
interaction_range = 50
force_strength = 0.1

# Aether particles
particles = []

# Particle class
class Particle:
    def __init__(self, x, y, type='positive'):
        self.x = x
        self.y = y
        self.type = type
        self.displacement = [0, 0]  # [dx, dy]

    def update_position(self):
        self.x += self.displacement[0]
        self.y += self.displacement[1]

        # Boundary conditions
        if self.x <= particle_radius or self.x >= WIDTH - particle_radius:
            self.displacement[0] *= -1
        if self.y <= particle_radius or self.y >= HEIGHT - particle_radius:
            self.displacement[1] *= -1

    def draw(self):
        color = RED if self.type == 'positive' else BLUE
        pygame.draw.circle(screen, color, (self.x, self.y), particle_radius)
        self.draw_displacement_vector()

    def draw_displacement_vector(self):
        end_x = self.x + self.displacement[0] * 10
        end_y = self.y + self.displacement[1] * 10
        pygame.draw.line(screen, GREEN, (self.x, self.y), (end_x, end_y), 2)

# Initialize particles
def create_particles():
    for _ in range(num_particles // 2):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        particles.append(Particle(x, y, 'positive'))
    for _ in range(num_particles // 2):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        particles.append(Particle(x, y, 'negative'))

create_particles()

# Function to update displacement vectors based on forces
def update_displacement_vectors():
    for particle in particles:
        fx, fy = 0, 0
        for other in particles:
            if particle != other:
                dx = other.x - particle.x
                dy = other.y - particle.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < interaction_range and distance > 0:  # Interaction range
                    if particle.type == other.type:
                        force = force_strength / distance  # Repulsive force
                    else:
                        force = -force_strength / distance  # Attractive force
                    fx += force * dx
                    fy += force * dy
        particle.displacement[0] = fx
        particle.displacement[1] = fy

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            type = 'positive' if event.button == 1 else 'negative'
            particles.append(Particle(x, y, type))

    screen.fill(WHITE)

    update_displacement_vectors()

    for particle in particles:
        particle.update_position()
        particle.draw()

    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
