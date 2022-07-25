import pygame
from sprite import *
from pygame.locals import *

class UI:
    def __init__(self):
        self.max_health = 57
        self.health = 0
        self.missed = 0
        self.draw_n_digits = 6
        self.winning_message = ""
        self.continue_message = "restart?"

        self.space_to_continue = False

        #health bar
        self.spr_healthbar_left = load_image("Assets/UI/Healthbar1.png")
        self.spr_healthbar_right = load_image("Assets/UI/Healthbar3.png")
        self.spr_healthbar_middle = load_image("Assets/UI/Healthbar2.png")
        self.health_bar = Sprite("", pos=(170 * SCALE_FACTOR, (SCREEN_HEIGHT - 8)  * SCALE_FACTOR)).set_image(self.get_healthbar_image())
        self.text_bot = Sprite("Assets/UI/TextBot.png", origin=(0, 1), pos=(0, WINDOW_HEIGHT)).hide()

        #black bars
        self.top_bar = Sprite("Assets/UI/BoarderTop.png", origin=(1, 0), pos=(WINDOW_WIDTH, 0))
        self.bot_bar = Sprite("Assets/UI/BoarderBot.png", origin=(0, 1), pos=(0, WINDOW_HEIGHT))
        black_bars = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), SRCALPHA)
        pygame.draw.rect(black_bars, (0, 0, 0), Rect(0, 0, WINDOW_WIDTH / 2, self.top_bar.rect.h))
        pygame.draw.rect(black_bars, (0, 0, 0), Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT - self.bot_bar.rect.h, WINDOW_WIDTH / 2, self.bot_bar.rect.h))
        self.black_bars = Sprite("").set_image(black_bars).hide()

        self.ready = Sprite("Assets/UI/Ready.png", origin=(0.5, 0.5), pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)).hide()
        self.start = Sprite("Assets/UI/start.png", origin=(0.5, 0.5), pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)).hide()
        self.text_top = Sprite("Assets/UI/TextTop.png").hide()

        #scroll numbers when incrimenting?
        self.missed_shots_text = Sprite("", pos=(61 * SCALE_FACTOR, 3 * SCALE_FACTOR)).set_image(self.get_missed_image()).hide()

        self.game_over = Sprite("Assets/UI/Game Over.png", origin=(0.5, 0.5), pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)).hide()
        self.winning_message_text = Sprite("", pos=(WINDOW_WIDTH / 2, (16 + SCREEN_HEIGHT / 2) * SCALE_FACTOR)).set_origin((0.5, 0))
        self.end_continue = Sprite("", origin=(0.5, 0), pos=(WINDOW_WIDTH / 2, (39 + SCREEN_HEIGHT / 2) *  SCALE_FACTOR)).hide()
    
    def draw(self, surface, time):
        self.black_bars.draw(surface)
        self.top_bar.draw(surface)
        self.bot_bar.draw(surface)
        self.text_top.draw(surface)
        self.text_bot.draw(surface)
        self.missed_shots_text.set_image(self.get_missed_image()).draw(surface)
        self.health_bar.set_image(self.get_healthbar_image()).draw(surface)
        self.game_over.draw(surface)
        self.winning_message_text.set_image(get_text_image(pixel_font, self.winning_message, 0.5, 0)).draw(surface)
        self.ready.draw(surface)
        self.start.draw(surface)
        self.end_continue.draw(surface)
    
    def get_healthbar_image(self):
        if self.health > 0:
            surf = pygame.Surface((self.health * self.spr_healthbar_middle.get_rect().w + self.spr_healthbar_left.get_rect().w + self.spr_healthbar_right.get_rect().w, \
                self.spr_healthbar_middle.get_rect().h), SRCALPHA)
            
            #self.spr_healthbar_left.move((0, 0))
            surf.blit(self.spr_healthbar_left, (0, 0))
            x = self.spr_healthbar_left.get_rect().w
            for _i in range(int(self.health) + 1):
                surf.blit(self.spr_healthbar_middle, (x, 0))
                x += self.spr_healthbar_middle.get_rect().w
            surf.blit(self.spr_healthbar_right, (self.spr_healthbar_left.get_rect().w + self.health * self.spr_healthbar_middle.get_rect().w, 0))
            return surf
        else:
            return pygame.Surface((0, 0))
    
    def set_health(self, ratio):
        self.health = ratio*self.max_health

    def get_missed_image(self):
        missed_string = str(self.missed)
        while len(missed_string) < self.draw_n_digits:
            missed_string = "0" + missed_string
        missed_string = missed_string[0 : self.draw_n_digits]
        return get_text_image(pixel_font, missed_string, 0, 0)

def get_text_image(fnt, text, align_x, align_y):
    char_rect = list(fnt.values())[0].get_rect()
    char_width = char_rect.w
    char_height = char_rect.h
    text = text.lower()
    lines = text.split('\n')
    max_line = max(len(line) for line in lines)
    surf = pygame.Surface((max_line * char_width, len(lines) * char_height), SRCALPHA)
    char_y = align_y * char_height
    for line in lines:
        char_x = align_x * (1 + max_line - len(line)) * char_width
        for character in line:
            surf.blit(fnt[character.upper()], (char_x - (align_x * char_width), char_y - align_y * char_height + 1))
            char_x += char_width
        char_y += char_height
    return surf

#fonts
pygame.font.init()
pixel_font = {}
for character in [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    '!', '?', ' ', '.', ',', '\'', '"',
]:
    character_to_filename = {
        '!' : 'zEX',
        '?' : 'zQU',
        ' ' : 'zSpace',
        '.' : 'zPeriod',
        ',' : 'zComma',
        '\'' : 'zApostrophe',
        '"' : 'zApostrophe',
    }
    key = ""
    if character in character_to_filename.keys():
        key = character_to_filename[character]
    else:
        key = character.upper()
    pixel_font[character.upper()] = load_image("Assets/UI/Text/" + key + ".png")