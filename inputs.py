class Inputs:
    def __init__(self):
        self.up = False
        self.left = False
        self.right = False
        self.down = False
        self.shoot = False

        self.locked = False
    
    def set_up(self, bool):
        if not self.locked:
            self.up = bool
    
    def set_left(self, bool):
        if not self.locked:
            self.left = bool
    
    def set_down(self, bool):
        if not self.locked:
            self.down = bool
    
    def set_right(self, bool):
        if not self.locked:
            self.right = bool
    
    def set_shoot(self, bool):
        if not self.locked:
            self.shoot = bool
    
    def lock(self):
        self.locked = True
    
    def unlock(self):
        self.locked = False