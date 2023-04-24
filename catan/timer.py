import pygame, json

from catan import NUMBER_FONT, BLACK


import pygame
import json

class Timer:
    def __init__(self, screen):
        self.screen = screen
        self.time = 15 * 60 * 1000  # 15 minutes in milliseconds
        self.paused = False
        self.remaining_time = self.time

    def update(self, dt):
        if not self.paused:
            self.remaining_time -= dt
            if self.remaining_time <= 0:
                self.remaining_time = 0
                self.paused = True

        # Convert milliseconds to minutes, seconds, and milliseconds
        minutes = int(self.remaining_time / 60000)
        seconds = int((self.remaining_time % 60000) / 1000)
        milliseconds = int(self.remaining_time % 1000)

        # Format the time as a string
        time_str = "{:02d}:{:02d}.{:03d}".format(minutes, seconds, milliseconds)

        # Render the time as text
        text = NUMBER_FONT.render(time_str, True, BLACK)

        # Display the time on the screen
        self.screen.blit(text, (1550, 250))



    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def save(self):
        data = {"time": self.time, "paused": self.paused, "remaining_time": self.remaining_time}
        with open("timer_data.txt", "w") as f:
            json.dump(data, f)

    def load(self):
        with open("timer_data.txt", "r") as f:
            data = json.load(f)
        self.time = data["time"]
        self.paused = data["paused"]
        self.remaining_time = data["remaining_time"]







