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

# Constants
K_F = 1.0
T_0 = 1.0
m_0 = 1.0
c = 3e8  # Speed of light
rho_0 = 1.0
DAMPING_FACTOR = 0.99
MAX_DISTANCE = 500  # Cap the maximum distance to prevent overflow

# Aether particle class
class AetherParticle:
    def __init__(self, x, y, charge):
        self.x = x
        self.y = y
        self.charge = charge  # +1 for positive, -1 for negative
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.rho_PD = random.uniform(0.5, 1.5)  # Random initial density
        self.rho_ND = random.uniform(0.5, 1.5)

    def update_position(self):
        self.vx += self.ax
        self.vy += self.ay
        self.vx *= DAMPING_FACTOR
        self.vy *= DAMPING_FACTOR
        self.x += self.vx
        self.y += self.vy
        self.ax, self.ay = 0, 0  # Reset acceleration after each update

    def apply_force(self, fx, fy):
        self.ax += fx / m_0
        self.ay += fy / m_0

    def draw(self):
        color = blue if self.charge > 0 else red
        # Ensure x and y are within reasonable bounds before drawing
        if abs(self.x) > width or abs(self.y) > height:
            print(f"Error drawing particle: x={self.x}, y={self.y}")
            return
        try:
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 5)
        except TypeError as e:
            print(f"Error drawing particle: {e}, x={self.x}, y={self.y}")

# Create a list of aether particles
particles = [AetherParticle(random.randint(100, 700), random.randint(100, 500), random.choice([-1, 1])) for _ in range(20)]

# Function to calculate forces based on displacement vectors and densities
def calculate_forces():
    for i, particle in enumerate(particles):
        fx, fy = 0, 0
        for j, other in enumerate(particles):
            if i != j:
                dx = other.x - particle.x
                dy = other.y - particle.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > MAX_DISTANCE:
                    continue  # Skip force calculation if distance is too large
                if distance > 0:
                    # Calculate displacement vectors and forces
                    P = (dx / distance, dy / distance)
                    rho_PD = particle.rho_PD
                    rho_ND = particle.rho_ND
                    U_PD = math.sqrt(particle.vx**2 + particle.vy**2)
                    U_ND = math.sqrt(other.vx**2 + other.vy**2)
                    
                    # Flow force
                    F_flow = K_F * ((rho_PD * (U_PD - (P[0] * particle.vx + P[1] * particle.vy))) - 
                                    (rho_ND * (U_ND - (P[0] * other.vx + P[1] * other.vy))))
                    fx += F_flow * P[0]
                    fy += F_flow * P[1]
                    
                    # Tension force
                    F_tension = T_0 * (rho_PD - rho_ND)
                    fx += F_tension * P[0]
                    fy += F_tension * P[1]
                    
                    # Electromagnetic force
                    force = (particle.charge * other.charge) / distance**2
                    fx += force * P[0]
                    fy += force * P[1]
        
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
