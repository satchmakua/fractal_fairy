import pygame
import math
import numpy as np
import time

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
        channel.play(sound)

    def stop(self):
        pygame.mixer.stop()

    def set_volume(self, volume):
        self.volume = volume

    def generate_sound(self):
        # Define the notes of the fantasy tune
        notes = ["C5", "E5", "G5", "B5", "C6", "B5", "G5", "E5"]
        note_durations = [1.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.5]

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

music = FantasyMusic()
music.set_volume(0.75)

music.play()
time.sleep(30)  # play music for 8 seconds
music.stop()

music.play()
time.sleep(12)  # play music for another 12 seconds
music.stop()

music.quit()

