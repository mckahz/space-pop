class Timer:
    def __init__(self, _max_time):
        self.time = _max_time
        self.max_time = _max_time
        self.active = False
    
    def get_ratio(self):
        return (self.max_time - self.time)/self.max_time
    
    def update(self, delta):
        if not self.active:
            return
        self.time -= delta
        if self.time <= 0:
            self.active = False
    
    def reset(self):
        self.time = self.max_time
        self.start()
    
    def start(self):
        self.active = True
    
    def stop(self):
        self.active = False
    
    def finish(self):
        self.time = 0