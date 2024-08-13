import pygame
import math
import random
import time
import pygame
import math
import numpy as np
import time

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
            # self.screen.fill((0, 0, 0))
            for particle in self.particles:
                particle.draw(self.screen)

            # Update the display
            pygame.display.flip()

            # Delay to control the frame rate
            self.clock.tick(60)
class FantasyMusic:
    def __init__(self):
        pygame.init()
        self.sample_rate = pygame.mixer.get_init()[0]
        self.duration = 5.0
        self.volume = 0.5

    def play(self):
        sound = self.generate_sound()
        channel = pygame.mixer.Channel(0)
        channel.set_volume(self.volume)
        channel.play(sound, loops=-1)

    def stop(self):
        pygame.mixer.stop()

    def set_volume(self, volume):
        self.volume = volume

    def generate_sound(self):
        # Define the notes of the fantasy tune
        notes = ["C5", "E5", "G5", "B5", "C6", "B5", "G5", "E5"]
        note_durations = [1.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0]

        # Define the frequency and duration of each note
        frequencies = [self.note_to_frequency(note) for note in notes]
        durations = [int(self.sample_rate * duration) for duration in note_durations]

        # Generate the sound wave for each note
        wave = []
        for i in range(len(frequencies)):
            wave.extend(self.generate_wave(frequencies[i], durations[i]))

        # Reshape the sound wave to a two-dimensional array with two channels
        sound_array = pygame.sndarray.array(wave)
        sound_array = sound_array.reshape((-1, 2))

        # Convert the sound wave to a Pygame sound object
        sound = pygame.sndarray.make_sound(sound_array)
        return sound

    def generate_wave(self, frequency, duration):
        wave = np.zeros((duration, 2), dtype=np.int16)
        for i in range(duration):
            t = float(i) / self.sample_rate
            value = math.sin(2.0 * math.pi * frequency * t)
            sample = int(value * 32767)
            wave[i] = np.array([sample, sample], dtype=np.int16)
        return wave

    def note_to_frequency(self, note):
        base_frequency = 440.0
        if note == "C0":
            return base_frequency / 16.0
        elif note == "C#0":
            return base_frequency / 15.0
        elif note == "D0":
            return base_frequency / 14.0
        elif note == "D#0":
            return base_frequency / 13.0
        elif note == "E0":
            return base_frequency / 12.0
        elif note == "F0":
            return base_frequency / 11.0
        elif note == "F#0":
            return base_frequency / 10.0
        elif note == "G0":
            return base_frequency / 9.0
        elif note == "G#0":
            return base_frequency / 8.0
        elif note == "A0":
            return base_frequency / 7.0
        elif note == "A#0":
            return base_frequency / 6.0
        elif note == "B0":
            return base_frequency / 5.0
        else:
            octave = int(note[1])
            semitones = 0
            if note[0] == "C":
                semitones = -9
            elif note[0] == "D":
                semitones = -7
            elif note[0] == "E":
                semitones = -5
            elif note[0] == "F":
                semitones = -4
            elif note[0] == "G":
                semitones = -2
            elif note[0] == "A":
                semitones = 0
            elif note[0] == "B":
                semitones = 2
            if len(note) == 3:
                if note[2] == "#":
                    semitones += 1
                elif note[2] == "b":
                    semitones -= 1
        frequency = base_frequency * (2.0 ** ((octave - 4) + (semitones / 12.0)))
        return frequency

    def quit(self):
        pygame.quit()


pygame.init()

# Set the size of the window
size = (800, 600)
screen = pygame.display.set_mode(size)

# Set up the tree parameters
start_pos = (size[0] // 2, size[1])
start_angle = -math.pi / 2
start_length = 5
angle_change = math.pi / 4
length_ratio = 0.7
num_generations = 8
branch_width = 5
leaf_size = 5

# Set up the trees
trees = []
tree_colors = [(252, 228, 236), (255, 251, 199), (206, 235, 214)]
tree_spacing = 200
for i in range(0, 1):
    trees.append((start_pos[0] + i * tree_spacing, start_pos[1]))

# Load the player sprite image and scale it down
player_image = pygame.image.load("player.png")
player_rect = player_image.get_rect()
player_scale = 20
player_image = pygame.transform.scale(player_image, (player_rect.width // player_scale, player_rect.height // player_scale))

# Set up the player variables
player_speed = 2
player_pos = [size[0] // 2, size[1] // 2]

# Define the tree drawing function
def draw_tree(position, angle, generation, growth, color):
    # Draw the branch
    length = start_length * (length_ratio ** generation) * growth
    end_pos = (position[0] + math.cos(angle) * length, position[1] + math.sin(angle) * length)
    pygame.draw.line(screen, color, position, end_pos, int(branch_width * (num_generations - generation) / num_generations))

    # Draw the leaves
    if generation == num_generations:
        for i in range(random.randint(1, 3)):
            leaf_pos = (end_pos[0] + random.randint(-leaf_size, leaf_size), end_pos[1] + random.randint(-leaf_size, leaf_size))
            pygame.draw.circle(screen, color, leaf_pos, leaf_size)

    # Recursive call for sub-branches
    if generation < num_generations:
        draw_tree(end_pos, angle - angle_change, generation + 1, growth, color)
        draw_tree(end_pos, angle + angle_change, generation + 1, growth, color)

# Start the main loop
running = True
growth = 1

music = FantasyMusic()
music.set_volume(0.75)
music.play()

# Start the main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player sprite continuously
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed

    # Draw the trees
    screen.fill((0, 0, 0))
    for i in range(len(trees)):
        color = tree_colors[i]
        draw_tree(trees[i], start_angle, 0, growth, color)

    # Draw the player sprite
    screen.blit(player_image, player_pos)

    # Update the display
    pygame.display.flip()

    # Increase the growth rate
    growth += 0.01

    # Add a delay
    time.sleep(0.01)

num_fireworks = 10
width = 800
height = 600

create_fireworks(num_fireworks, width, height)

# Draw the text to the screen
screen.blit(text, text_rect)
pygame.display.flip()
pygame.display.update()
# Wait for three seconds
pygame.time.wait(3000)

# Stop the music and quit Pygame
music.stop()
music.quit()
pygame.quit()
