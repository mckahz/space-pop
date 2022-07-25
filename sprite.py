import pygame
from pygame.locals import *
from constants import *

class Sprite:
    def __init__(self, path, speed = 0, **kwargs):
        spr_frames = []
        if path != "":
            if speed == 0:
                spr_frames.append(load_image(path))
            else:
                i = 1
                while True:
                    try:
                        spr_frames.append(load_image(path + str(i) + ".png"))
                    except:
                        break
                    i += 1

        self.frames = spr_frames
        self.rect = self.frames[0].get_rect() if len(self.frames) > 0 else Rect(0, 0, 0, 0)
        self.origin_x = 0
        self.origin_y = 0
        self.rel = True
        self.x = 0
        self.y = 0
        for (key, value) in kwargs.items():
            if key == "origin":
                self.set_origin(value)
            elif key == "rel":
                self.rel = value
            elif key == "pos":
                (x, y) = value
                self.x = x
                self.y = y

        self.speed = speed
        self.visible = True

        self.loop = True
        self.times_looped = 0
        self.previous_frame = 0

        self.time_offset = 0

    def show(self):
        self.visible = True
        return self
    
    def hide(self):
        self.visible = False
        return self

    def move(self, to):
        (to_x, to_y) = to
        self.x = to_x
        self.y = to_y
        return self

    def draw(self, surface, time = 0):
        if not self.visible:
            return
        time += self.time_offset
        frame = self.get_current_frame(time)
        if frame == 0 and self.previous_frame != 0:
            self.times_looped += 1
        self.previous_frame = frame
        offset_x = self.origin_x * self.rect.w if self.rel else self.origin_x
        offset_y = self.origin_y * self.rect.h if self.rel else self.origin_y
        surface.blit(self.frames[self.get_current_frame(time)], (self.x - offset_x, self.y - offset_y))
    
    def set_index(self, to, time):
        if self.speed != 0:
            self.time_offset = to / self.speed - time
        return self

    def set_loop(self, looping):
        self.loop = looping
        if not looping:
            self.previous_frame = 0
            self.times_looped = 0
        return self
    
    def set_origin(self, to):
        (origin_x, origin_y) = to
        self.origin_x = origin_x
        self.origin_y = origin_y
        return self

    def get_current_frame(self, time):
        if self.finished():
            return len(self.frames) - 1
        frame = int(self.speed * time)
        return frame % len(self.frames)
    
    def finished(self):
        val = not self.loop and self.times_looped > 0
        return val
    
    def set_image(self, img):
        self.frames.clear()
        self.frames.append(img)
        self.rect = self.frames[0].get_rect() if len(self.frames) > 0 else Rect(0, 0, 0, 0)
        return self

def load_image(path):
    img = pygame.image.load(path).convert_alpha()
    spr_rect = img.get_rect()
    return pygame.transform.scale(img, (SCALE_FACTOR * spr_rect.w, SCALE_FACTOR * spr_rect.h))