
class TimedCycle:
    def __init__(self, max_frame, ticks, movements, start_frame=0):
        self.current_tick = 0
        self.max_frame = max_frame
        self.frame = start_frame
        self.movements = movements
        self.max_ticks = ticks
        self.config = (max_frame, start_frame, movements, ticks)

        self.one = False

    def tick(self):
        self.current_tick += 1
        if self.current_tick > self.max_ticks[self.frame]:
            self.frame += 1
            self.current_tick = 0
            if self.frame >= self.max_frame:
                self.frame = 0
                self.one = True

    def get_movement(self):
        return self.movements[self.frame]

    def get_frame(self):
        return self.frame

    def reset(self):
        self.current_tick = 0
        self.max_frame, self.frame, self.movements, self.max_ticks = self.config
        self.one = False
