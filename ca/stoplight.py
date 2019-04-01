
class Stoplight():

    def __init__(self, is_green, green_time=None, red_time=None):
        self.is_green = is_green
        if green_time is not None:
            self.green_time = green_time
        else:
            self.green_time = 10
        if red_time is not None:
            self.red_time = red_time
        else:
            self.red_time = 5
        self.counter = 0
        
    def set_green(self):
        self.is_green = True
        self.counter = 0

    def set_red(self):
        self.is_green = False
        self.counter = 0

    def timestep(self):
        self.counter += 1
        if self.is_green and self.counter >= self.green_time:
            self.set_red()
        elif not self.is_green and self.counter >= self.red_time:
            self.set_green()

        
