
import pygame
import random

pygame.display.set_caption("Multi Bingo")
screen = pygame.display.set_mode((0,0))
screen.fill([0,0,0])
pygame.mouse.set_visible(False)

meter = pygame.image.load('graphics/assets/register_cover.png').convert()
eb = pygame.image.load('spot_lite/assets/arrow.png').convert_alpha()
exb = pygame.image.load('spot_lite/assets/extra_ball.png').convert_alpha()
o1 = pygame.image.load('spot_lite/assets/odds_gi.png').convert_alpha()
o = pygame.image.load('spot_lite/assets/odds.png').convert_alpha()
o10 = pygame.image.load('spot_lite/assets/odds10.png').convert_alpha()
c = pygame.image.load('spot_lite/assets/corners.png').convert_alpha()
number = pygame.image.load('spot_lite/assets/number.png').convert_alpha()
tilt = pygame.image.load('spot_lite/assets/tilt.png').convert_alpha()

class scorereel():
    """ Score Reels are used to count replays """
    def __init__(self, pos, image):
        self.position = pos
        self.default_y = self.position[1]
        self.image = pygame.image.load(image).convert()

reel1 = scorereel([625,782], "graphics/assets/green_reel.png")
reel10 = scorereel([605,782], "graphics/assets/green_reel.png")
reel100 = scorereel([587,782], "graphics/assets/green_reel.png")

def display(s, replays=0, menu=False):
    
    meter.set_colorkey((255,0,252))
    meter_position = [577,782]

    screen.blit(reel1.image, reel1.position)
    screen.blit(reel10.image, reel10.position)
    screen.blit(reel100.image, reel100.position)
    screen.blit(meter, meter_position)

    backglass_position = [0, 0]
    backglass = pygame.Surface(screen.get_size(), flags=pygame.SRCALPHA)
    backglass.fill((0, 0, 0))
    if menu == True:
        backglass = pygame.image.load('spot_lite/assets/spot_lite_menu.png')
    else:
        if (s.game.anti_cheat.status == True):
            backglass = pygame.image.load('spot_lite/assets/spot_lite_gi.png')
        else:
            backglass = pygame.image.load('spot_lite/assets/spot_lite_off.png')
    backglass = pygame.transform.scale(backglass, (720, 1280))
    
    screen.blit(backglass, backglass_position)

    if s.game.extra_ball.position == 1:
        eb_position = [32,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 2:
        eb_position = [58,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 3:
        eb_position = [85,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 4:
        eb_position = [111,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 5:
        eb_position = [136,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 6:
        eb_position = [161,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 7:
        eb_position = [188,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 8:
        eb_position = [215,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 9:
        eb_position = [241,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 10:
        eb_position = [267,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 11:
        eb_position = [293,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 12:
        eb_position = [319,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 13:
        eb_position = [377,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 14:
        eb_position = [403,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 15:
        eb_position = [428,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 16:
        eb_position = [455,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 17:
        eb_position = [481,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 18:
        eb_position = [507,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 19:
        eb_position = [533,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 20:
        eb_position = [559,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 21:
        eb_position = [586,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 22:
        eb_position = [612,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 23:
        eb_position = [634,934]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 24:
        eb_position = [663,934]
        screen.blit(eb, eb_position)

    if s.game.extra_ball.position >= 12:
        eb_position = [29,979]
        screen.blit(exb, eb_position)
    if s.game.extra_ball.position >= 24:
        eb_position = [374,979]
        screen.blit(exb, eb_position)

    if s.game.odds.position > 0:
        odds_position = [19,371]
        screen.blit(o1, odds_position)
        if s.game.odds.position == 1:
            odds_position = [154,371]
            screen.blit(o, odds_position)
        if s.game.odds.position == 2:
            odds_position = [206,371]
            screen.blit(o, odds_position)
        if s.game.odds.position == 3:
            odds_position = [258,371]
            screen.blit(o, odds_position)
        if s.game.odds.position == 4:
            odds_position = [311,371]
            screen.blit(o, odds_position)
        if s.game.odds.position == 5:
            odds_position = [363,371]
            screen.blit(o, odds_position)
        if s.game.odds.position == 6:
            odds_position = [415,371]
            screen.blit(o, odds_position)
        if s.game.odds.position == 7:
            odds_position = [468,371]
            screen.blit(o, odds_position)
        if s.game.odds.position == 8:
            odds_position = [521,371]
            screen.blit(o, odds_position)
        if s.game.odds.position == 9:
            odds_position = [573,371]
            screen.blit(o, odds_position)
        if s.game.odds.position == 10:
            odds_position = [625,371]
            screen.blit(o10, odds_position)

    if s.game.corners.status == True:
        corners_position = [37,741]
        screen.blit(c, corners_position)

    if s.game.tilt.status == False:
        if s.holes:
            if 1 in s.holes:
                number_position = [199,772]
                screen.blit(number, number_position)
            if 2 in s.holes:
                number_position = [199,706]
                screen.blit(number, number_position)
            if 3 in s.holes:
                number_position = [465,838]
                screen.blit(number, number_position)
            if 4 in s.holes:
                number_position = [398,571]
                screen.blit(number, number_position)
            if 5 in s.holes:
                number_position = [333,838]
                screen.blit(number, number_position)
            if 6 in s.holes:
                number_position = [464,571]
                screen.blit(number, number_position)
            if 7 in s.holes:
                number_position = [265,841]
                screen.blit(number, number_position)
            if 8 in s.holes:
                number_position = [466,772]
                screen.blit(number, number_position)
            if 9 in s.holes:
                number_position = [199,573]
                screen.blit(number, number_position)
            if 10 in s.holes:
                number_position = [201,838]
                screen.blit(number, number_position)
            if 11 in s.holes:
                number_position = [333,772]
                screen.blit(number, number_position)
            if 12 in s.holes:
                number_position = [398,707]
                screen.blit(number, number_position)
            if 13 in s.holes:
                number_position = [200,639]
                screen.blit(number, number_position)
            if 14 in s.holes:
                number_position = [331,640]
                screen.blit(number, number_position)
            if 15 in s.holes:
                number_position = [331,571]
                screen.blit(number, number_position)
            if 16 in s.holes:
                number_position = [333,705]
                screen.blit(number, number_position)
            if 17 in s.holes:
                number_position = [463,707]
                screen.blit(number, number_position)
            if 18 in s.holes:
                number_position = [267,705]
                screen.blit(number, number_position)
            if 19 in s.holes:
                number_position = [266,637]
                screen.blit(number, number_position)
            if 20 in s.holes:
                number_position = [398,637]
                screen.blit(number, number_position)
            if 21 in s.holes:
                number_position = [398,771]
                screen.blit(number, number_position)
            if 22 in s.holes:
                number_position = [267,771]
                screen.blit(number, number_position)
            if 23 in s.holes:
                number_position = [397,839]
                screen.blit(number, number_position)
            if 24 in s.holes:
                number_position = [267,572]
                screen.blit(number, number_position)
            if 25 in s.holes:
                number_position = [465,639]
                screen.blit(number, number_position)

    if s.game.tilt.status == True:
        tilt_position = [82,882]
        screen.blit(tilt, tilt_position)

    pygame.display.update()

def eb_animation(num):
    global screen
    if num == 24:
        eb_position = [32,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 23:
        eb_position = [58,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 22:
        eb_position = [85,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 21:
        eb_position = [111,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 20:
        eb_position = [136,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 19:
        eb_position = [161,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 18:
        eb_position = [188,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 17:
        eb_position = [215,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 16:
        eb_position = [241,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 15:
        eb_position = [267,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 14:
        eb_position = [293,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 13:
        eb_position = [319,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 12:
        eb_position = [377,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 11:
        eb_position = [403,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 10:
        eb_position = [428,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 9:
        eb_position = [455,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 8:
        eb_position = [481,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 7:
        eb_position = [507,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 6:
        eb_position = [533,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 5:
        eb_position = [559,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 4:
        eb_position = [586,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 3:
        eb_position = [612,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 2:
        eb_position = [634,934]
        screen.blit(eb, eb_position)
        pygame.display.update()
    if num == 1:
        eb_position = [663,934]
        screen.blit(eb, eb_position)
        pygame.display.update()

def feature_animation(num):
    global screen
    if num == 2 or num == 1:
        c_position = [37,741]
        c = pygame.image.load('spot_lite/assets/corners.png').convert_alpha()
        screen.blit(c, c_position)
        pygame.display.update()

def odds_animation(num):
    global screen
    if num == 10:
        odds_position = [154,371]
        screen.blit(o, odds_position)
        pygame.display.update()
    if num == 9:
        odds_position = [206,371]
        screen.blit(o, odds_position)
        pygame.display.update()
    if num == 8:
        odds_position = [258,371]
        screen.blit(o, odds_position)
        pygame.display.update()
    if num == 7:
        odds_position = [311,371]
        screen.blit(o, odds_position)
        pygame.display.update()
    if num == 6:
        odds_position = [363,371]
        screen.blit(o, odds_position)
        pygame.display.update()
    if num == 5:
        odds_position = [415,371]
        screen.blit(o, odds_position)
        pygame.display.update()
    if num == 4:
        odds_position = [468,371]
        screen.blit(o, odds_position)
        pygame.display.update()
    if num == 3:
        odds_position = [521,371]
        screen.blit(o, odds_position)
        pygame.display.update()
    if num == 2:
        odds_position = [573,371]
        screen.blit(o, odds_position)
        pygame.display.update()
    if num == 1:
        odds_position = [625,371]
        screen.blit(o, odds_position)
        pygame.display.update()