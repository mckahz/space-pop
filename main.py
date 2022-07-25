import pygame
import maths

pygame.init()
pygame.display.set_caption("Space Pop - Pygame v2.0.1")
pygame.display.set_icon(pygame.image.load("Assets/icon.png"))

from constants import *

display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

import sys
import random
import ease
from inputs import *
from objects import *
from sprite import *
from ui import *
from timeline import *

from pygame.locals import *


def get_winning_message(missed):
    shots_to_message = {
        0: "Perfect Score!\nNo Shots Missed!",
        2: "You missed 2 shots!\nSo close!",
        4: "4 Shots missed!\nNot Bad!",
    }
    return shots_to_message[missed] if missed in shots_to_message.keys() else \
        "You missed " + str(missed) + " shots!\n" + random.choice([
            "I couldn't do any better.",
            "That first one totally hit!",
            "You can do better!",
            "But what do I know!",
            "Better luck next time!",
            "As if!"
        ])

def get_intro_timeline(**kwargs):
    snd_engine = kwargs["snd_engine"]
    player = kwargs["player"]
    ui = kwargs["ui"]
    balloon = kwargs["balloon"]
    inputs = kwargs["inputs"]
    snd_music_intro = kwargs["snd_music_intro"]
    snd_music_loop = kwargs["snd_music_loop"]
    
    def play_engine(t, kwargs):
        snd_engine.play(-1, 0, 1)
    
    def move_in_player(t, kwargs):
        def point_at(t):
            (from_pos_x, from_pos_y) = kwargs["from_pos"]
            (to_pos_x, to_pos_y) = kwargs["to_pos"]
            return ((to_pos_x - from_pos_x) * ease.out_quad(t) + from_pos_x, (to_pos_y - from_pos_y) * ease.out_quart(t) + from_pos_y)
        (then_x, then_y) = point_at(t - 0.01)
        (now_x, now_y) = point_at(t)
        dy = now_y-then_y
        dx = now_x-then_x
        ratio = dy/dx if dx != 0 else maths.sign(dy)
        threshold = 0.3
        if ratio < -threshold:
            player.moving_up = True
            player.moving_down = False
        elif ratio > threshold:
            player.moving_up = False
            player.moving_down = True
        else:
            player.moving_up = False
            player.moving_down = False
        player.x = now_x
        player.y = now_y
    
    def flash_ready(t, kwargs):
        ui.ready.visible = maths.floor(t*2*kwargs["n"]) % 2 == 0
    
    def set_sprite_visible(t, kwargs):
        kwargs["sprite"].visible = kwargs["visible"]
    
    def enable_balloon_jumping(t, kwargs):
        balloon.can_jump = True
        balloon.allow_oob = False
        balloon.jump_timer.reset()
    
    def enable_balloon_falling(t, kwargs):
        balloon.falling = True
    
    def unlock_controls(t, kwargs):
        inputs.unlock()
    
    def move_object(t, kwargs):
        obj = kwargs["obj"]
        ease_func = ease.linear
        if "ease_func" in kwargs.keys():
            ease_func = kwargs["ease_func"]
        (x, y) = maths.lerp_pos(kwargs["from_pos"], kwargs["to_pos"], ease_func(t))
        obj.x = x
        obj.y = y
    
    def fill_health(t, kwargs):
        ui.set_health(ease.in_out_quad(t))
    
    def draw_missed(t, kwargs):
        ui.draw_n_digits = round(kwargs["to"] * t)
    
    def draw_black_bars(t, kwargs):
        ui.black_bars.show()
    
    def start_intro(t, kwargs):
        snd_music_intro.play()
    
    def start_loop(t, kwargs):
        if player.can_shoot:
            snd_music_loop.play(-1)
    
    draw_bars = Timeline.par([
        Timeline(0.42, move_object, obj=ui.top_bar, from_pos=(0, ui.top_bar.y), to_pos=(ui.top_bar.x, ui.top_bar.y), ease_func=ease.out_quad_snap),
        Timeline(0.42, move_object, obj=ui.bot_bar, from_pos=(WINDOW_WIDTH, ui.bot_bar.y), to_pos=(ui.bot_bar.x, ui.bot_bar.y), ease_func=ease.out_quad_snap),
        Timeline.seq([
            Timeline.wait(0.2),
            Timeline(0, draw_black_bars),
        ])
    ])
    
    draw_text = Timeline.seq([
        Timeline(0, set_sprite_visible, sprite=ui.text_top, visible=True),
        Timeline(0, set_sprite_visible, sprite=ui.text_bot, visible=True),
        Timeline.par([
            Timeline(0.3, move_object, obj=ui.text_top, from_pos=(ui.text_top.x, -ui.text_top.rect.h), to_pos=(ui.text_top.x, ui.text_top.x), ease_func=ease.out_cube),
            Timeline(0.3, move_object, obj=ui.text_bot, from_pos=(ui.text_bot.x, WINDOW_HEIGHT + ui.text_bot.rect.h), to_pos=(ui.text_bot.x, ui.text_bot.y), ease_func=ease.out_cube),
            Timeline(0.3, move_object, obj=ui.health_bar, from_pos=(ui.health_bar.x, WINDOW_HEIGHT + ui.text_bot.rect.h + (ui.health_bar.y - ui.text_bot.y)), to_pos=(ui.health_bar.x, ui.health_bar.y), ease_func=ease.out_cube),
            Timeline(0.5, fill_health),
        ]),
        Timeline(0, set_sprite_visible, sprite=ui.missed_shots_text, visible=True),
        Timeline(0.7, draw_missed, to=ui.draw_n_digits),
    ])

    move_player = Timeline.seq([
        Timeline(0, play_engine),
        Timeline(1, move_in_player, from_pos=(-2 * SCALE_FACTOR, (SCREEN_HEIGHT / 2 - 33) * SCALE_FACTOR), to_pos=(66 * SCALE_FACTOR, WINDOW_HEIGHT / 2)),
    ])

    flash_and_show_ready = Timeline.seq([
        Timeline(0.3, flash_ready, n=2),
        Timeline(0, set_sprite_visible, sprite=ui.ready, visible=True),
        Timeline.wait(1.6),
        Timeline(0, set_sprite_visible, sprite=ui.ready, visible=False),
        Timeline.wait(0.3),
        Timeline(0, set_sprite_visible, sprite=ui.start, visible=True),
    ])

    play_music = Timeline.seq([
        Timeline(0, start_intro),
        Timeline.wait(snd_music_intro.get_length()),
        Timeline(0, start_loop),
    ])

    setup_stage = Timeline.seq([
        #fade in the menu
        draw_bars,
        #bar text
        draw_text,
        Timeline.wait(0.3),
        #move the objects in
        move_player,
        Timeline.wait(0.6),
        flash_and_show_ready,
        Timeline(0, unlock_controls, inputs=inputs),
        Timeline(0, enable_balloon_falling),
        Timeline(0, enable_balloon_jumping),
        Timeline.wait(1),
        Timeline(0, set_sprite_visible, sprite=ui.start, visible=False),
    ])

    return Timeline.par([setup_stage, play_music])

def get_outro_timeline(**kwargs):
    bullets = kwargs["bullets"]
    balloon = kwargs["balloon"]
    snd_hit = kwargs["snd_hit"]
    snd_explosion = kwargs["snd_explosion"]
    snd_music_loop = kwargs["snd_music_loop"]
    snd_music_intro = kwargs["snd_music_intro"]
    ui = kwargs["ui"]
    player = kwargs["player"]
    effects = kwargs["effects"]
    winning_message = get_winning_message(ui.missed)
    type_speed = 0.08

    def display_game_over(t, kwargs):
        ui.game_over.visible = True
    
    def destroy_bullets(t, kwargs):
        for bullet in kwargs["bullets"]:
            effect = bullet.spr_bullet_disappear.set_loop(False).set_index(0, pygame.time.get_ticks() / 1000).move((bullet.x, bullet.y))
            effect.set_loop(False)
            effects.append(effect)
        bullets.clear()
    
    def flash_ready(t, kwargs):
        ui.game_over.visible = maths.floor(t*2*kwargs["n"]) % 2 == 0
    
    def prevent_shooting(t, kwargs):
        player.can_shoot = False
    
    def damage_balloon(t, kwargs):
        balloon.sprite.visible = False
        balloon.can_jump = False
        balloon.gravity = 0
        balloon.vel_y = 0
        snd_hit.play()
        effect = balloon.spr_damage.set_loop(False).set_index(0, pygame.time.get_ticks() / 1000).move((balloon.x, balloon.y))
        effects.append(effect)
    
    def destroy_balloon(t, kwargs):
        effect = balloon.spr_death.set_loop(False).set_index(0, pygame.time.get_ticks() / 1000).move((balloon.x, balloon.y))
        snd_explosion.play()
        effects.append(effect)
    
    def show_winning_message(t, kwargs):
        ui.winning_message = winning_message[0 : int(len(winning_message) * t)]
    
    def show_continue(t, kwargs):
        ui.end_continue.set_image(
            get_text_image(pixel_font, ui.continue_message[0 : int(len(ui.continue_message) * t)], 0.5, 0)
        ).show()
    
    def let_space_be_continue(t, kwargs):
        ui.space_to_continue = True
    
    def empty_health(t, kwargs):
        ui.set_health(ease.invert(ease.in_out_power(2.36)(t)))
    
    def stop_music(t, kwargs):
        snd_music_loop.fadeout(kwargs["time"])
        snd_music_intro.fadeout(kwargs["time"])
    
    balloon_timeline = Timeline.seq([
        Timeline(0, damage_balloon, balloon=balloon, effects=effects),
        Timeline.wait(len(balloon.spr_damage.frames)/balloon.spr_damage.speed - 0.001),
        Timeline(0, destroy_balloon, balloon=balloon, effects=effects),
    ])

    show_text = Timeline.seq([
        Timeline.wait(5),
        Timeline(0.1, flash_ready, n=1),
        Timeline.wait(2),
        Timeline(0, display_game_over),
        Timeline(len(winning_message) * type_speed, show_winning_message),
        Timeline.wait(1.5),
        Timeline(len(ui.continue_message) * type_speed, show_continue),
        Timeline(0, let_space_be_continue),
    ])

    timeline = Timeline.par([
        Timeline(0, destroy_bullets, bullets=bullets, effects=effects),
        Timeline(0, prevent_shooting, player=player),
        Timeline(0, stop_music, time = 200),
        Timeline(0.42, empty_health, ui=ui),
        balloon_timeline,
        show_text
    ])

    return timeline

def main():
    #sound
    snd_music_intro = pygame.mixer.Sound("Assets/Sound/GameTheme(Intro).wav")
    snd_music_loop = pygame.mixer.Sound("Assets/Sound/GameTheme(Loop).wav")
    snd_engine = pygame.mixer.Sound("Assets/Sound/SFX/Engine.wav")
    snd_explosion = pygame.mixer.Sound("Assets/Sound/SFX/Explosion.wav")
    snd_hit = pygame.mixer.Sound("Assets/Sound/SFX/Hit.wav")
    snd_shoot = pygame.mixer.Sound("Assets/Sound/SFX/Shoot3.wav")

    #objects
    inputs = Inputs()
    player = Player()
    balloon = Balloon()
    backgrounds = [
        Background(Sprite("Assets/BG/Stars.png"), 2.4 * SCALE_FACTOR),
        Background(Sprite("Assets/BG/SmallPlanet1.png", pos=(20 * SCALE_FACTOR, 5 * SCALE_FACTOR)), 4 * SCALE_FACTOR),
        Background(Sprite("Assets/BG/SmallPlanet2.png", pos=(209 * SCALE_FACTOR, 48 * SCALE_FACTOR)), 6 * SCALE_FACTOR),
        Background(Sprite("Assets/BG/Big Planet.png", origin=(0, 1), pos=(0, WINDOW_HEIGHT)), 12 * SCALE_FACTOR),
    ]
    ui = UI()
    bullets = []
    effects = []
    flashes =[]

    #time
    slow_motion = 1
    clock = pygame.time.Clock()
    intro_timeline = get_intro_timeline(
        snd_engine=snd_engine,
        player=player,
        ui=ui,
        balloon=balloon,
        inputs=inputs,
        snd_music_intro=snd_music_intro,
        snd_music_loop=snd_music_loop
    ).start(pygame.time.get_ticks() / (slow_motion * 1000))
    outro_timeline = Timeline.wait(0)
    
    inputs.lock()


    while True:
        clock.tick()
        delta = clock.get_time() / (slow_motion * 1000)
        current_time = pygame.time.get_ticks() / (slow_motion * 1000)

        #handle input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN or event.type == KEYUP:
                pressed = event.type == KEYDOWN
                if event.key == K_UP:
                    inputs.set_up(pressed)
                elif event.key == K_DOWN:
                    inputs.set_down(pressed)
                elif event.key == K_LEFT:
                    inputs.set_left(pressed)
                elif event.key == K_RIGHT:
                    inputs.set_right(pressed)
                elif event.key == K_SPACE:
                    inputs.set_shoot(pressed)
                    if ui.space_to_continue and inputs.shoot:
                        pygame.mixer.stop()
                        main()

        for background in backgrounds:
            background.update(delta)
        player.update(inputs, delta)
        balloon.update(delta)
        for bullet in bullets:
            bullet.update(delta)
        for effect in effects:
            if effect.finished():
                effects.remove(effect)
        for flash in flashes:
            if flash[1].finished():
                flashes.remove(flash)
            flash[1].move((player.x - 9 * SCALE_FACTOR, player.y + flash[0] * SCALE_FACTOR))

        #create bullets
        player.shoot_timer.update(delta)
        if not inputs.shoot:
            player.shoot_timer.finish()
        elif player.can_shoot and not player.shoot_timer.active:
            snd_shoot.stop()
            snd_shoot.play()
            for i in player.gun_offsets:
                bullet = Bullet()
                bullet.x = player.x - 3 * SCALE_FACTOR
                bullet.y = player.y + i * SCALE_FACTOR
                bullet.vel_x += balloon.terminal_vel * 10
                bullet.vel_y += player.vel_y * 0.3
                bullets.append(bullet)

                flash = (i, Sprite("Assets/Ship/Flash/Flash", 9, origin=(0, 0.5)).set_loop(False).set_index(0, current_time))
                flashes.append(flash)

            player.shoot_timer.reset()
            player.shoot_timer.start()

        #collide with balloon
        for (i, bullet) in enumerate(bullets):
            if not bullet.missed and bullet.x > balloon.x + balloon.radius + bullet.radius:
                bullet.missed = True
                ui.missed += 1
            if bullet.x > WINDOW_WIDTH + bullet.sprite.rect.w:
                bullets.pop(i)
            elif maths.distance((balloon.x, balloon.y), (bullet.x, bullet.y)) < balloon.radius + bullet.radius:
                outro_timeline = get_outro_timeline(
                    current_time=current_time,
                    bullets=bullets,
                    balloon=balloon,
                    snd_hit=snd_hit,
                    snd_explosion=snd_explosion,
                    snd_music_loop=snd_music_loop,
                    snd_music_intro=snd_music_intro,
                    ui=ui,
                    player=player,
                    effects=effects,
                )
                outro_timeline.start(current_time)
                break

        #timeline animations (placed after the update events to override them)
        intro_timeline.play(current_time)
        outro_timeline.play(current_time)

        display.fill(BACKGROUND_COLOR)
        
        for background in backgrounds:
            background.draw(display, current_time)
        player.draw(display, current_time)
        balloon.draw(display, current_time)
        for bullet in bullets:
            bullet.draw(display, current_time)
        for effect in effects:
            effect.draw(display, current_time)
        for flash in flashes:
            flash[1].draw(display, current_time)
        ui.draw(display, current_time)

        pygame.display.update()

main()
