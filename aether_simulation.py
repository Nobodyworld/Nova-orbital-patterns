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
DAMPING_FACTOR = 0.9
MAX_DISTANCE = 200  # Cap the maximum distance to prevent overflow
MAX_VELOCITY = 5  # Cap the maximum velocity to prevent overflow
MAX_POSITION = 800  # Cap the maximum position to prevent overflow

# Preon masses (in arbitrary units)
MASS_A = 45.6
MASS_B = 34.8
MASS_C = 67.9

# Aether particle class
class AetherParticle:
    def __init__(self, x, y, preon_type):
        self.x = x
        self.y = y
        self.preon_type = preon_type  # A, B, or C
        self.vx = random.uniform(-1, 1)  # Smaller initial velocity
        self.vy = random.uniform(-1, 1)
        self.ax = 0
        self.ay = 0
        self.rho_PD = random.uniform(0.5, 1.5)  # Random initial density
        self.rho_ND = random.uniform(0.5, 1.5)
        self.mass = self.get_mass()
        self.charge = self.get_charge()

    def get_mass(self):
        if self.preon_type == 'A':
            return MASS_A
        elif self.preon_type == 'B':
            return MASS_B
        elif self.preon_type == 'C':
            return MASS_C

    def get_charge(self):
        if self.preon_type == 'A':
            return 0
        elif self.preon_type == 'B':
            return -1
        elif self.preon_type == 'C':
            return 2

    def update_position(self):
        self.vx += self.ax
        self.vy += self.ay
        
        # Apply damping factor
        self.vx *= DAMPING_FACTOR
        self.vy *= DAMPING_FACTOR

        # Cap the velocity
        self.vx = max(min(self.vx, MAX_VELOCITY), -MAX_VELOCITY)
        self.vy = max(min(self.vy, MAX_VELOCITY), -MAX_VELOCITY)

        # Update positions
        self.x += self.vx
        self.y += self.vy

        # Cap the position
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            print(f"Resetting particle due to extreme position: x={self.x}, y={self.y}")
            self.reset()

        # Reset acceleration after each update
        self.ax, self.ay = 0, 0

    def apply_force(self, fx, fy):
        self.ax += fx / self.mass
        self.ay += fy / self.mass

    def reset(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 500)
        self.vx = random.uniform(-1, 1)  # Reset with smaller initial velocity
        self.vy = random.uniform(-1, 1)
        self.ax = 0
        self.ay = 0

    def draw(self):
        color = blue if self.charge > 0 else red
        try:
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 5)
        except (ValueError, OverflowError) as e:
            print(f"Error drawing particle: {e}, x={self.x}, y={self.y}")
            self.reset()

# Create a list of aether particles
particles = [AetherParticle(random.randint(100, 700), random.randint(100, 500), random.choice(['A', 'B', 'C'])) for _ in range(20)]

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
                    rho_ND = other.rho_ND
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
