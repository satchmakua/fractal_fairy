import pygame
import random
import math
import time

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def create_fireworks(num_fireworks, width, height):
    # Initialize Pygame
    pygame.init()

    # Set the size of the window
    size = (width, height)
    screen = pygame.display.set_mode(size)

    # Set the caption of the window
    pygame.display.set_caption("Fireworks")

    # Create a list of fireworks
    fireworks = []
    for i in range(num_fireworks):
        fireworks.append(create_firework(width, height))

    # Start the main loop
    clock = pygame.time.Clock()
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Clear the screen
        screen.fill(BLACK)

        # Update and draw the fireworks
        for i in range(len(fireworks)):
            fireworks[i].update()
            fireworks[i].draw(screen)

            # Create new fireworks at the end of the trail
            if fireworks[i].done():
                fireworks[i] = create_firework(width, height)

        # Update the display
        pygame.display.update()

        # Tick the clock
        clock.tick(60)

def create_firework(width, height):
    # Choose a random position and color for the firework
    x = random.randint(0, width)
    y = random.randint(0, height // 2)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Choose a random number of particles and create them
    num_particles = random.randint(30, 50)
    particles = []
    for i in range(num_particles):
        particles.append(create_particle(x, y, color))

    # Create the firework
    return Firework(particles)

def create_particle(x, y, color):
    # Choose a random velocity and angle for the particle
    speed = random.randint(5, 15)
    angle = random.uniform(0, 2 * math.pi)

    # Create the particle
    return Particle(x, y, speed * math.cos(angle), -speed * math.sin(angle), color)

class Firework:
    def __init__(self, particles):
        self.particles = particles

    def update(self):
        # Update each particle
        for i in range(len(self.particles)):
            self.particles[i].update()

    def draw(self, screen):
        # Draw each particle
        for i in range(len(self.particles)):
            self.particles[i].draw(screen)

    def done(self):
        # Check if all particles have stopped moving
        for i in range(len(self.particles)):
            if self.particles[i].speed > 0:
                return False
        return True

class Particle:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.speed = math.sqrt(vx ** 2 + vy ** 2)

    def update(self):
        # Update the position and velocity of the particle
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.speed = math.sqrt(self.vx ** 2 + self.vy ** 2)

    def draw(self, screen):
        # Draw the particle on the screen
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

    def is_offscreen(self, screen_width, screen_height):
        # Check if the particle is off the screen
        return self.x < 0 or self.x > screen_width or self.y > screen_height

    def draw_firework(self, pos, color):
        # Generate random number of particles for the firework
        num_particles = random.randint(30, 50)
        
        # Generate particles for the firework
        particles = []
        for i in range(num_particles):
            particle = Particle(pos[0], pos[1], color)
            particle.vel = self.generate_firework_velocity()
            particles.append(particle)
            
        # Add the particles to the list of all particles
        self.particles += particles

    def generate_firework_velocity(self):
        # Generate random velocity for the firework particles
        speed = random.randint(3, 5)
        angle = random.uniform(0, 2 * math.pi)
        vx = speed * math.cos(angle)
        vy = -speed * math.sin(angle)
        return [vx, vy]

    def run(self):
        # Start the game loop
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.draw_firework(pygame.mouse.get_pos(), self.random_color())

            # Update the particles and remove any that are dead
            for particle in self.particles:
                particle.update()
                if particle.is_dead():
                    self.particles.remove(particle)

            # Draw the particles
            self.screen.fill((0, 0, 0))
            for particle in self.particles:
                particle.draw(self.screen)

            # Update the display
            pygame.display.flip()

            # Delay to control the frame rate
            self.clock.tick(60)

if __name__ == '__main__':
    num_fireworks = 10
    width = 800
    height = 600
    create_fireworks(num_fireworks, width, height)