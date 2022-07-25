from constants import *
from sprite import *
from timer import *
import random
import maths

class Background:
    def __init__(self, sprite, parallax = 0):
        self.sprite = sprite
        self.parallax = parallax
        self.repeat_x = self.sprite.rect.w + 12 * SCALE_FACTOR
        if self.sprite.rect.w < WINDOW_WIDTH:
            self.repeat_x += WINDOW_WIDTH
    
    def update(self, delta):
        self.sprite.x -= self.parallax * delta
        if self.sprite.x < -self.repeat_x:
            self.sprite.x += self.repeat_x

    def draw(self, surface, time):
        self.sprite.draw(surface, time)
        self.sprite.move((self.sprite.x + self.repeat_x, self.sprite.y))
        self.sprite.draw(surface, time)
        self.sprite.move((self.sprite.x - self.repeat_x, self.sprite.y))

class Bullet:
    def __init__(self):
        self.radius = 3 * SCALE_FACTOR
        self.missed = False

        self.x = 0
        self.y = 0

        self.vel_x = 0
        self.vel_y = 0

        self.spr_bullet = Sprite("Assets/Ship/Bullet.png", origin=(0.5, 0.5))
        self.spr_bullet_disappear = Sprite("Assets/Ship/BulletDis/BulletDis", 15, origin=(0.5, 0.5))
        self.sprite = self.spr_bullet

    def update(self, delta):
        self.x += self.vel_x * delta
        self.y += self.vel_y * delta
    
    def draw(self, surface, time):
        self.sprite.move((self.x, self.y))
        self.sprite.draw(surface, time)

class Balloon:
    def __init__(self):
        self.radius = 8 * SCALE_FACTOR

        self.jump_vel = -37 * SCALE_FACTOR
        self.vel_y = 0
        self.gravity = 25 * SCALE_FACTOR
        self.terminal_vel = 33 * SCALE_FACTOR

        self.jump_timer = Timer(0.5)
        self.can_jump = False
        self.allow_oob = True
        self.falling = False
        
        self.spr_idle = Sprite("Assets/Balloon/Idle/BalloonIdle", 5, origin=(0.5, 0.4))
        self.spr_damage = Sprite("Assets/Balloon/Damage/BalloonDMG", 10, origin=(0.5, 0.4))
        self.spr_death = Sprite("Assets/Balloon/Death/BalloonDeath", 7, origin=(0.5, 0.4))
        self.sprite = self.spr_idle

        self.x = (SCREEN_WIDTH - 33) * SCALE_FACTOR
        self.y = WINDOW_HEIGHT / 2
    
    def update(self, delta):
        OFF = 25 * SCALE_FACTOR
        BOTTOM = WINDOW_HEIGHT - OFF
        TOP = OFF
        
        #clamp
        if not self.allow_oob:
            if self.y < TOP:
                self.y = TOP
                self.vel_y = 0
            elif self.y > BOTTOM:
                self.y = BOTTOM
                self.vel_y = self.jump_vel
        
        #jump
        self.jump_timer.update(delta)
        if self.can_jump and not self.jump_timer.active:
            self.jump_timer = Timer(random.uniform(2.6, 3.1))
            self.jump_timer.start()
            self.vel_y = self.jump_vel
        
        #move
        if self.falling:
            self.vel_y += self.gravity * delta
            self.vel_y = min(self.terminal_vel, self.vel_y)
            self.y += self.vel_y * delta
    
    def draw(self, surface, time):
        self.sprite.move((self.x, self.y))
        self.sprite.draw(surface, time)

class Player:
    def __init__(self):
        self.x = -50 * SCALE_FACTOR
        self.y = WINDOW_HEIGHT / 2

        self.acc = 5
        self.speed = 133 * SCALE_FACTOR
        self.vel_x = 0
        self.vel_y = 0

        self.can_shoot = True
        self.shoot_timer = Timer(0.3)

        self.spr_up = Sprite("Assets/Ship/ship up.png", origin=(1, 0.5))
        self.spr_down = Sprite("Assets/Ship/ship down.png", origin=(1, 0.5))
        self.spr_idle = Sprite("Assets/Ship/ship idle.png", origin=(1, 0.5))
        self.sprite = self.spr_idle

        self.spr_flame = Sprite("Assets/Ship/Tail Flame/Flame", 12, origin=(1, 0.5))
        self.spr_muzzle_flash = Sprite("Assets/Ship/Flash", 12, origin=(0.5, 0.5))

        self.gun_offsets = [-7, 7]

        self.moving_up = False
        self.moving_down = False
    
    def update(self, inputs, delta):
        #move player
        #find the direction the player is moving in
        (dir_x, dir_y) = (0, 0)
        if inputs.left:
            dir_x -= 1
        if inputs.right:
            dir_x += 1
        if inputs.up:
            dir_y -= 1
        if inputs.down:
            dir_y += 1
        (dir_x, dir_y) = maths.normalize((dir_x, dir_y))

        #keep the player within bounds or ease the velocity to input velocity
        if not inputs.locked:
            (X_MIN, X_MAX) = (47 * SCALE_FACTOR, (SCREEN_HEIGHT / 2 + 95) * SCALE_FACTOR)
            Y_OFF = 50 * SCALE_FACTOR
            (Y_MIN, Y_MAX) = (Y_OFF, WINDOW_HEIGHT - Y_OFF)
            PADDING = 25 * SCALE_FACTOR
            self.vel_x += (dir_x * self.speed - self.vel_x) * self.acc * delta
            if self.x < X_MIN:
                self.vel_x = max(self.vel_x, -self.speed * (self.x + PADDING - X_MIN)/PADDING)
            elif self.x > X_MAX:
                self.vel_x = min(self.vel_x, self.speed * (X_MAX + PADDING - self.x)/PADDING)
            self.vel_y += (dir_y * self.speed - self.vel_y) * self.acc * delta
            if self.y < Y_MIN:
                self.vel_y = max(self.vel_y, -self.speed * (self.y + PADDING - Y_MIN)/PADDING)
            elif self.y > Y_MAX:
                self.vel_y = min(self.vel_y, self.speed * (Y_MAX + PADDING - self.y)/PADDING)
        
        #move the player
        self.x += self.vel_x * delta
        self.y += self.vel_y * delta

        #say which way I'm trying to move
        threshold = 10 * SCALE_FACTOR
        self.moving_up = inputs.up and not inputs.down and self.vel_y < -threshold
        self.moving_down = inputs.down and not inputs.up and self.vel_y > threshold

        if self.moving_up:
            self.gun_offsets = [-6, 7]
        elif self.moving_down:
            self.gun_offsets = [-6, 7]
        else:
            self.gun_offsets = [-7, 7]
    
    def draw(self, surface, time):
        spr = 0
        if self.moving_up:
            spr = self.spr_up
        elif self.moving_down:
            spr = self.spr_down
        else:
            spr = self.spr_idle
        spr.move((self.x, self.y))
        spr.draw(surface)
        self.spr_flame.move((self.x - self.sprite.rect.w, self.y))
        self.spr_flame.draw(surface, time)