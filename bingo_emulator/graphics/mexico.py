
import pygame
import random

pygame.display.set_caption("Multi Bingo")
screen = pygame.display.set_mode((0,0))
screen.fill([0,0,0])
pygame.mouse.set_visible(False)

meter = pygame.image.load('graphics/assets/silver_register_cover.png').convert()
sc_arrow = pygame.image.load('mexico/assets/sc_arrow.png').convert_alpha()
sc = pygame.image.load('mexico/assets/super_card.png').convert_alpha()
eb = pygame.image.load('mexico/assets/eb.png').convert_alpha()
extra_ball = pygame.image.load('mexico/assets/extra_ball.png').convert_alpha()
extra_balls = pygame.image.load('mexico/assets/extra_balls.png').convert_alpha()
o1 = pygame.image.load('mexico/assets/odds1.png').convert_alpha()
o2 = pygame.image.load('mexico/assets/odds2.png').convert_alpha()
o3 = pygame.image.load('mexico/assets/odds3.png').convert_alpha()
o4 = pygame.image.load('mexico/assets/odds4.png').convert_alpha()
o5 = pygame.image.load('mexico/assets/odds5.png').convert_alpha()
o6 = pygame.image.load('mexico/assets/odds6.png').convert_alpha()
o7 = pygame.image.load('mexico/assets/odds7.png').convert_alpha()
o8 = pygame.image.load('mexico/assets/odds8.png').convert_alpha()
star = pygame.image.load('mexico/assets/rollover.png').convert_alpha()
number = pygame.image.load('mexico/assets/number.png').convert_alpha()
sc_number = pygame.image.load('mexico/assets/sc_number.png').convert_alpha()
tilt = pygame.image.load('mexico/assets/tilt.png').convert_alpha()
select_now = pygame.image.load('mexico/assets/select_now.png').convert_alpha()
red_number = pygame.image.load('mexico/assets/red_number.png').convert_alpha()
red_sc_number = pygame.image.load('mexico/assets/red_sc_number.png').convert_alpha()
s_number = pygame.image.load('mexico/assets/spotted_numbers.png').convert_alpha()
s_arrow = pygame.image.load('mexico/assets/selection_arrow.png').convert_alpha()
before_fourth = pygame.image.load('mexico/assets/before_fourth.png').convert_alpha()
super_selection = pygame.image.load('mexico/assets/super_selection.png').convert_alpha()
select_feature = pygame.image.load('mexico/assets/select_feature.png').convert_alpha()
red_select_feature = pygame.image.load('mexico/assets/red_select_feature.png').convert_alpha()
three_four = pygame.image.load('mexico/assets/3_as_4.png').convert_alpha()
special_card = pygame.image.load('mexico/assets/special_card.png').convert_alpha()
letter_me = pygame.image.load('mexico/assets/letter_me.png').convert_alpha()
letter_xi = pygame.image.load('mexico/assets/letter_xi.png').convert_alpha()
letter_co = pygame.image.load('mexico/assets/letter_co.png').convert_alpha()
lite_a_name = pygame.image.load('mexico/assets/lite_a_name.png').convert_alpha()
return_arrow = pygame.image.load('mexico/assets/return_arrow.png').convert_alpha()
ball_return = pygame.image.load('mexico/assets/return.png').convert_alpha()
bg_menu = pygame.image.load('mexico/assets/mexico_menu.png')
bg_gi = pygame.image.load('mexico/assets/mexico_gi.png')
bg_off = pygame.image.load('mexico/assets/mexico_off.png')

class scorereel():
    """ Score Reels are used to count replays """
    def __init__(self, pos, image):
        self.position = pos
        self.default_y = self.position[1]
        self.image = pygame.image.load(image).convert()

reel1 = scorereel([113,847], "graphics/assets/green_reel.png")
reel10 = scorereel([94,847], "graphics/assets/green_reel.png")
reel100 = scorereel([75,847], "graphics/assets/green_reel.png")

def display(s, replays=0, menu=False):
    
    meter.set_colorkey((255,0,252))
    meter_position = [65,845]

    screen.blit(reel1.image, reel1.position)
    screen.blit(reel10.image, reel10.position)
    screen.blit(reel100.image, reel100.position)
    screen.blit(meter, meter_position)

    backglass_position = [0, 0]
    backglass = pygame.Surface(screen.get_size(), flags=pygame.SRCALPHA)
    backglass.fill((0, 0, 0))
    if menu == True:
        screen.blit(bg_menu, backglass_position)
    else:
        if (s.game.anti_cheat.status == True):
            screen.blit(bg_gi, backglass_position)
        else:
            screen.blit(bg_off, backglass_position)

    if s.game.tilt.status == True:
        p = [229,259]
        screen.blit(letter_me, p)
        p = [340,259]
        screen.blit(letter_xi, p)
        p = [408,261]
        screen.blit(letter_co, p)
    else:
        p = [221,311]
        screen.blit(lite_a_name, p)

    if s.game.super_card.position == 1:
        p = [38,422]
        screen.blit(sc_arrow, p)
    if s.game.super_card.position == 2:
        p = [72,422]
        screen.blit(sc_arrow, p)
    if s.game.super_card.position == 3:
        p = [110,422]
        screen.blit(sc_arrow, p)
    if s.game.super_card.position == 4:
        p = [146,422]
        screen.blit(sc_arrow, p)
    if s.game.super_card.position == 5:
        p = [544,422]
        screen.blit(sc_arrow, p)
    if s.game.super_card.position == 6:
        p = [580,422]
        screen.blit(sc_arrow, p)
    if s.game.super_card.position == 7:
        p = [620,422]
        screen.blit(sc_arrow, p)
    if s.game.super_card.position == 8:
        p = [656,422]
        screen.blit(sc_arrow, p)

    if s.game.super_card.position >= 4:
        p = [45,237]
        screen.blit(sc, p)

    if s.game.super_card.position >= 8:
        p = [554,238]
        screen.blit(sc, p)

    if s.game.extra_ball.position == 1:
        eb_position = [99,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 2:
        eb_position = [132,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 3:
        eb_position = [167,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 4:
        eb_position = [202,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 5:
        eb_position = [238,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 6:
        eb_position = [275,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 7:
        eb_position = [311,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 8:
        eb_position = [347,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 9:
        eb_position = [379,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 10:
        eb_position = [415,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 11:
        eb_position = [455,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 12:
        eb_position = [491,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 13:
        eb_position = [527,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 14:
        eb_position = [561,984]
        screen.blit(eb, eb_position)
    if s.game.extra_ball.position == 15:
        eb_position = [596,984]
        screen.blit(eb, eb_position)

    if s.game.extra_ball.position >= 5 and s.game.extra_ball.position < 10:
        eb_pos = [96,1018]
        screen.blit(extra_ball, eb_pos)
    if s.game.extra_ball.position >= 10 and s.game.extra_ball.position < 15:
        eb_pos = [275,1018]
        screen.blit(extra_ball, eb_pos)
    if s.game.extra_ball.position == 15:
        eb_pos = [456,1018]
        screen.blit(extra_ball, eb_pos)

    if s.game.odds.position > 0:
        if s.game.odds.position == 1:
            odds_position = [177,827]
            screen.blit(o1, odds_position)
        if s.game.odds.position == 2:
            odds_position = [237,827]
            screen.blit(o2, odds_position)
        if s.game.odds.position == 3:
            odds_position = [283,830]
            screen.blit(o3, odds_position)
        if s.game.odds.position == 4:
            odds_position = [332,827]
            screen.blit(o4, odds_position)
        if s.game.odds.position == 5:
            odds_position = [456,827]
            screen.blit(o5, odds_position)
        if s.game.odds.position == 6:
            odds_position = [508,827]
            screen.blit(o6, odds_position)
        if s.game.odds.position == 7:
            odds_position = [558,824]
            screen.blit(o7, odds_position)
        if s.game.odds.position == 8:
            odds_position = [610,824]
            screen.blit(o8, odds_position)

    if s.game.red_star.status == True:
        rs_position = [637,987]
        screen.blit(star, rs_position)

    if s.game.corners.status == True:
        corners_position = [365,640]
        screen.blit(three_four, corners_position)

    if s.game.tilt.status == False:
        if s.holes:
            if 1 in s.holes:
                number_position = [225,521]
                screen.blit(number, number_position)
                number_position = [550,328]
                screen.blit(sc_number, number_position)
                number_position = [65,547]
                screen.blit(sc_number, number_position)
            if 2 in s.holes:
                number_position = [225,466]
                screen.blit(number, number_position)
            if 3 in s.holes:
                number_position = [448,577]
                screen.blit(number, number_position)
                number_position = [92,282]
                screen.blit(sc_number, number_position)
            if 4 in s.holes:
                number_position = [280,358]
                screen.blit(number, number_position)
                number_position = [596,378]
                screen.blit(sc_number, number_position)
                number_position = [63,592]
                screen.blit(sc_number, number_position)
            if 5 in s.holes:
                number_position = [337,577]
                screen.blit(number, number_position)
            if 6 in s.holes:
                number_position = [450,359]
                screen.blit(number, number_position)
                number_position = [620,594]
                screen.blit(sc_number, number_position)
            if 7 in s.holes:
                number_position = [282,576]
                screen.blit(number, number_position)
                number_position = [599,280]
                screen.blit(sc_number, number_position)
            if 8 in s.holes:
                number_position = [448,412]
                screen.blit(number, number_position)
            if 9 in s.holes:
                number_position = [225,356]
                screen.blit(number, number_position)
                number_position = [44,329]
                screen.blit(sc_number, number_position)
                number_position = [619,546]
                screen.blit(sc_number, number_position)
            if 10 in s.holes:
                number_position = [224,413]
                screen.blit(number, number_position)
                number_position = [598,328]
                screen.blit(sc_number, number_position)
            if 11 in s.holes:
                number_position = [225,577]
                screen.blit(number, number_position)
                number_position = [137,328]
                screen.blit(sc_number, number_position)
                number_position = [646,280]
                screen.blit(sc_number, number_position)
            if 12 in s.holes:
                number_position = [393,466]
                screen.blit(number, number_position)
                number_position = [43,378]
                screen.blit(sc_number, number_position)
                number_position = [111,546]
                screen.blit(sc_number, number_position)
            if 13 in s.holes:
                number_position = [338,521]
                screen.blit(number, number_position)
                number_position = [645,329]
                screen.blit(sc_number, number_position)
            if 14 in s.holes:
                number_position = [339,414]
                screen.blit(number, number_position)
                number_position = [137,376]
                screen.blit(sc_number, number_position)
            if 15 in s.holes:
                number_position = [337,356]
                screen.blit(number, number_position)
                number_position = [551,280]
                screen.blit(sc_number, number_position)
            if 16 in s.holes:
                number_position = [338,468]
                screen.blit(number, number_position)
            if 17 in s.holes:
                number_position = [449,522]
                screen.blit(number, number_position)
                number_position = [549,377]
                screen.blit(sc_number, number_position)
                number_position = [572,593]
                screen.blit(sc_number, number_position)
            if 18 in s.holes:
                number_position = [282,466]
                screen.blit(number, number_position)
                number_position = [139,281]
                screen.blit(sc_number, number_position)
                number_position = [644,377]
                screen.blit(sc_number, number_position)
            if 19 in s.holes:
                number_position = [282,413]
                screen.blit(number, number_position)
            if 20 in s.holes:
                number_position = [394,413]
                screen.blit(number, number_position)
            if 21 in s.holes:
                number_position = [394,522]
                screen.blit(number, number_position)
            if 22 in s.holes:
                number_position = [281,522]
                screen.blit(number, number_position)
            if 23 in s.holes:
                number_position = [393,577]
                screen.blit(number, number_position)
                number_position = [44,283]
                screen.blit(sc_number, number_position)
                number_position = [572,545]
                screen.blit(sc_number, number_position)
            if 24 in s.holes:
                number_position = [393,358]
                screen.blit(number, number_position)
                number_position = [91,376]
                screen.blit(sc_number, number_position)
                number_position = [112,594]
                screen.blit(sc_number, number_position)
            if 25 in s.holes:
                number_position = [451,466]
                screen.blit(number, number_position)
                number_position = [91,328]
                screen.blit(sc_number, number_position)

    if s.game.tilt.status == True:
        tilt_position = [80,795]
        screen.blit(tilt, tilt_position)

    if s.game.selection_feature.position == 2:
        p = [100,699]
        screen.blit(s_arrow, p)
    if s.game.selection_feature.position == 3:
        p = [140,699]
        screen.blit(s_arrow, p)
    if s.game.selection_feature.position == 4:
        p = [180,699]
        screen.blit(s_arrow, p)
    if s.game.selection_feature.position >= 5:
        p = [215,694]
        screen.blit(s_number, p)
    if s.game.selection_feature.position >= 6:
        p = [254,694]
        screen.blit(s_number, p)
    if s.game.selection_feature.position >= 7:
        p = [293,694]
        screen.blit(s_number, p)
    if s.game.selection_feature.position >= 8:
        p = [332,694]
        screen.blit(s_number, p)
    if s.game.selection_feature.position >= 9:
        p = [372,694]
        screen.blit(s_number, p)
    if s.game.selection_feature.position >= 10:
        p = [410,694]
        screen.blit(s_number, p)
    if s.game.selection_feature.position >= 11:
        p = [451,694]
        screen.blit(s_number, p)

    if (s.game.select_spots.status == True or s.game.selection_feature_relay.status == True):
        if s.game.before_fourth.status == True:
            if s.game.ball_count.position == 3:
                s.cancel_delayed(name="blink")
                blink([s,1,1])
            else:
                s.cancel_delayed(name="blink")

    if (s.game.select_spots.status == True or s.game.selection_feature_relay.status == True):
        if s.game.before_fifth.status == True:
            if s.game.ball_count.position == 4:
                s.cancel_delayed(name="blink")
                blink([s,1,1])
            else:
                s.cancel_delayed(name="blink")

    if s.game.before_fourth.status == True and (s.game.selection_feature.position > 3 or s.game.selection_feature_relay.status == True):
        p = [7,695]
        screen.blit(before_fourth, p)
    if s.game.before_fifth.status == True and (s.game.selection_feature.position > 3 or s.game.selection_feature_relay.status == True):
        p = [624,695]
        screen.blit(before_fourth, p)

    if s.game.before_fourth.status == True:
        if s.game.ball_count.position < 4:
            if s.game.select_spots.status == True:
                if s.game.selection_feature.position >= 5:
                    if s.game.spotted.position == 0:
                        #19
                        number_position = [282,413]
                        screen.blit(red_number, number_position)
                if s.game.selection_feature.position >= 6:
                    if s.game.spotted.position == 1:
                        #20
                        number_position = [394,413]
                        screen.blit(red_number, number_position)
                if s.game.selection_feature.position >= 7:
                    if s.game.spotted.position == 2:
                        #21
                        number_position = [394,522]
                        screen.blit(red_number, number_position)
                if s.game.selection_feature.position >= 8:
                    if s.game.spotted.position == 3:
                        #22
                        number_position = [281,522]
                        screen.blit(red_number, number_position)
                if s.game.selection_feature.position >= 9:
                    if s.game.spotted.position == 4:
                        #16
                        number_position = [338,468]
                        screen.blit(red_number, number_position)
                if s.game.selection_feature.position >= 10:
                    if s.game.spotted.position == 5:
                        #25
                        number_position = [451,466]
                        screen.blit(red_number, number_position)
                        number_position = [91,328]
                        screen.blit(red_sc_number, number_position)
                if s.game.selection_feature.position >= 11:
                    if s.game.spotted.position == 6:
                        #10
                        number_position = [224,413]
                        screen.blit(red_number, number_position)
                        number_position = [598,328]
                        screen.blit(red_sc_number, number_position)
            if s.game.selection_feature_relay.status == True:
                if s.game.spotted.position == 7:
                    p = [100,737]
                    screen.blit(red_select_feature, p)
                if s.game.spotted.position == 8:
                    p = [205,737]
                    screen.blit(red_select_feature, p)
                if s.game.spotted.position == 9:
                    p = [415,737]
                    screen.blit(red_select_feature, p)
                if s.game.spotted.position == 10:
                    p = [519,737]
                    screen.blit(red_select_feature, p)

    if s.game.before_fifth.status == True:
        if s.game.ball_count.position < 5:
            if s.game.select_spots.status == True:
                if s.game.selection_feature.position >= 5:
                    if s.game.spotted.position == 0:
                        #19
                        number_position = [282,413]
                        screen.blit(red_number, number_position)
                if s.game.selection_feature.position >= 6:
                    if s.game.spotted.position == 1:
                        #20
                        number_position = [394,413]
                        screen.blit(red_number, number_position)
                if s.game.selection_feature.position >= 7:
                    if s.game.spotted.position == 2:
                        #21
                        number_position = [394,522]
                        screen.blit(red_number, number_position)
                if s.game.selection_feature.position >= 8:
                    if s.game.spotted.position == 3:
                        #22
                        number_position = [281,522]
                        screen.blit(red_number, number_position)
                if s.game.selection_feature.position >= 9:
                    if s.game.spotted.position == 4:
                        #16
                        number_position = [338,468]
                        screen.blit(red_number, number_position)
                if s.game.selection_feature.position >= 10:
                    if s.game.spotted.position == 5:
                        #25
                        number_position = [451,466]
                        screen.blit(red_number, number_position)
                        number_position = [91,328]
                        screen.blit(red_sc_number, number_position)
                if s.game.selection_feature.position >= 11:
                    if s.game.spotted.position == 6:
                        #10
                        number_position = [224,413]
                        screen.blit(red_number, number_position)
                        number_position = [598,328]
                        screen.blit(red_sc_number, number_position)
            if s.game.selection_feature_relay.status == True:
                if s.game.spotted.position == 7:
                    p = [100,737]
                    screen.blit(red_select_feature, p)
                if s.game.spotted.position == 8:
                    p = [205,737]
                    screen.blit(red_select_feature, p)
                if s.game.spotted.position == 9:
                    p = [415,737]
                    screen.blit(red_select_feature, p)
                if s.game.spotted.position == 10:
                    p = [519,737]
                    screen.blit(red_select_feature, p)
                
    if s.game.selection_feature_relay.status == True:
        p = [100,737]
        screen.blit(select_feature, p)
        p = [205,737]
        screen.blit(select_feature, p)
        p = [312,734]
        screen.blit(super_selection, p)
        p = [415,737]
        screen.blit(select_feature, p)
        p = [519,737]
        screen.blit(select_feature, p)


    if s.game.three_as_four.status == True:
        p = [254,642]
        screen.blit(three_four, p)

    if s.game.left_special_card.status == True:
        p = [62,507]
        screen.blit(special_card, p)
    if s.game.right_special_card.status == True:
        p = [570,505]
        screen.blit(special_card, p)

    if s.game.eb_play.status == True:
        p = [25,995]
        screen.blit(extra_balls, p)

    if s.game.letter_me.status == True:
        p = [229,259]
        screen.blit(letter_me, p)
    if s.game.letter_xi.status == True:
        p = [340,259]
        screen.blit(letter_xi, p)
    if s.game.letter_co.status == True:
        p = [408,261]
        screen.blit(letter_co, p)

    if s.game.ball_return.position == 1:
        p = [185,949]
        screen.blit(return_arrow, p)
    if s.game.ball_return.position == 2:
        p = [218,949]
        screen.blit(return_arrow, p)
    if s.game.ball_return.position == 3:
        p = [249,949]
        screen.blit(return_arrow, p)
    if s.game.ball_return.position == 4:
        p = [283,949]
        screen.blit(return_arrow, p)
    if s.game.ball_return.position == 5:
        p = [315,949]
        screen.blit(return_arrow, p)
    if s.game.ball_return.position == 6:
        p = [346,949]
        screen.blit(return_arrow, p)
    if s.game.ball_return.position == 7:
        p = [380,945]
        screen.blit(ball_return, p)

    pygame.display.update()

def blink(args):
    dirty_rects = []
    s = args[0]
    b = args[1]
    sn = args[2]

    if b == 0:
        if sn == 1:
            p = [491,694]
            dirty_rects.append(screen.blit(select_now, p))
        pygame.display.update(dirty_rects)
    else:
        dirty_rects.append(screen.blit(bg_gi, (491,694), pygame.Rect(491,694,132,39)))
        pygame.display.update(dirty_rects)
    b = not b

    args = [s,b,sn]

    s.delay(name="blink", delay=0.1, handler=blink, param=args)

def eb_animation(args):
    global screen

    dirty_rects = []
    s = args[0]
    num = args[1]
    if s.game.extra_ball.position < 5:
        dirty_rects.append(screen.blit(bg_gi, (96,1018), pygame.Rect(96,1018,172,32)))
    if s.game.extra_ball.position < 10:
        dirty_rects.append(screen.blit(bg_gi, (275,1018), pygame.Rect(275,1018,172,32)))
    if s.game.extra_ball.position < 15:
        dirty_rects.append(screen.blit(bg_gi, (456,1018), pygame.Rect(456,1018,172,32)))
        dirty_rects.append(screen.blit(bg_gi, (596,984), pygame.Rect(596,984,29,32)))
    pygame.display.update(dirty_rects)

    if num in [1,9,17,4,12,15,21]:
        if s.game.extra_ball.position < 5:
            p = [96,1018]
            dirty_rects.append(screen.blit(extra_ball, p))
            pygame.display.update(dirty_rects) 
    elif num in [2,10,18,5,7,13,16,22]:
        if s.game.extra_ball.position < 10:
            p = [275,1018]
            dirty_rects.append(screen.blit(extra_ball, p))
            pygame.display.update(dirty_rects)
    elif num in [3,11,19,6,8,14,20,23]:
        if s.game.extra_ball.position < 15:
            p = [456,1018]
            dirty_rects.append(screen.blit(extra_ball, p))
            p = [596,984]
            dirty_rects.append(screen.blit(eb, p))
            pygame.display.update(dirty_rects)

def clear_odds(s, num):
    global screen
    dirty_rects = []
    if s.game.odds.position != 1:
        dirty_rects.append(screen.blit(bg_gi, (177,827), pygame.Rect(177,827,83,101)))
    if s.game.odds.position != 2:
        dirty_rects.append(screen.blit(bg_gi, (237,827), pygame.Rect(237,827,67,99)))
    if s.game.odds.position != 3:
        dirty_rects.append(screen.blit(bg_gi, (283,830), pygame.Rect(283,830,74,99)))
    if s.game.odds.position != 4:
        dirty_rects.append(screen.blit(bg_gi, (332,827), pygame.Rect(332,827,74,103)))
    if s.game.odds.position != 5:
        dirty_rects.append(screen.blit(bg_gi, (456,827), pygame.Rect(456,827,80,99)))
    if s.game.odds.position != 6:
        dirty_rects.append(screen.blit(bg_gi, (508,827), pygame.Rect(508,827,80,100)))
    if s.game.odds.position != 7:
        dirty_rects.append(screen.blit(bg_gi, (558,824), pygame.Rect(558,824,81,108)))
    if s.game.odds.position != 8:
        dirty_rects.append(screen.blit(bg_gi, (610,824), pygame.Rect(610,824,96,104)))

    pygame.display.update(dirty_rects)

def draw_odds_animation(s, num):
    global screen
    dirty_rects = []
    if num in [0,11,17]:
        if s.game.odds.position != 1:
            p = [177,827]
            dirty_rects.append(screen.blit(o1, p))
            pygame.display.update(dirty_rects)
            return
    if num in [1,10,18]:
        if s.game.odds.position != 2:
            p = [237,827]
            dirty_rects.append(screen.blit(o2, p))
            pygame.display.update(dirty_rects)
            return
    if num in [4,12,19]:
        if s.game.odds.position != 3:
            p = [283,830]
            dirty_rects.append(screen.blit(o3, p))
            pygame.display.update(dirty_rects)
            return
    if num in [3,9,20]:
        if s.game.odds.position != 4:
            p = [332,827]
            dirty_rects.append(screen.blit(o4, p))
            pygame.display.update(dirty_rects)
            return
    if num in [5,13,21]:
        if s.game.odds.position != 5:
            p = [456,827]
            dirty_rects.append(screen.blit(o5, p))
            pygame.display.update(dirty_rects)
            return
    if num in [6,14,22]:
        if s.game.odds.position != 6:
            p = [508,827]
            dirty_rects.append(screen.blit(o6, p))
            pygame.display.update(dirty_rects)
            return
    if num in [7,16,23]:
        if s.game.odds.position != 7:
            p = [558,824]
            dirty_rects.append(screen.blit(o7, p))
            pygame.display.update(dirty_rects)
            return
    if num in [8,15,24]:
        if s.game.odds.position != 8:
            p = [610,824]
            dirty_rects.append(screen.blit(o8, p))
            pygame.display.update(dirty_rects)
            return

def odds_animation(args):
    global screen

    dirty_rects = []
    s = args[0]
    num = args[1]

    clear_odds(s, num)

    draw_odds_animation(s, num)

def clear_mixers(s):
    global screen
    dirty_rects = []

    if s.game.super_card.position < 4:
        dirty_rects.append(screen.blit(bg_gi, (45,237), pygame.Rect(45,237,133,34)))
    if s.game.super_card.position < 8:
        dirty_rects.append(screen.blit(bg_gi, (554,238), pygame.Rect(554,238,133,34)))
    if s.game.corners.status == False:
        dirty_rects.append(screen.blit(bg_gi, (365,640), pygame.Rect(365,640,103,42)))
    if s.game.ball_return.position != 7:
        dirty_rects.append(screen.blit(bg_gi, (380,945), pygame.Rect(380,945,298,38)))
    if s.game.red_star.status == False:
        dirty_rects.append(screen.blit(bg_gi, (637,987), pygame.Rect(637,987,63,60)))
    if s.game.left_special_card.status == False:
        dirty_rects.append(screen.blit(bg_gi, (62,507), pygame.Rect(62,507,94,38)))
    if s.game.right_special_card.status == False:
        dirty_rects.append(screen.blit(bg_gi, (570,505), pygame.Rect(570,505,94,38)))
    if s.game.selection_feature_relay.status == False:
        dirty_rects.append(screen.blit(bg_gi, (312,734), pygame.Rect(312,734,99,49)))
    pygame.display.update(dirty_rects)
    return

def animate_mixer1(s):
    global screen
    dirty_rects = []
    if s.game.super_card.position < 4:
        p = [45,237]
        dirty_rects.append(screen.blit(sc, p))
        pygame.display.update(dirty_rects)
        return


def animate_mixer2(s):
    global screen
    dirty_rects = []
    if s.game.super_card.position < 8:
        p = [554,238]
        dirty_rects.append(screen.blit(sc, p))
    if s.game.left_special_card.status == False:
        p = [62,507]
        dirty_rects.append(screen.blit(special_card, p))
    pygame.display.update(dirty_rects)
    return

def animate_mixer3(s):
    global screen
    dirty_rects = []
    if s.game.corners.status == False:
        p = [365,640]
        dirty_rects.append(screen.blit(three_four, p))
    if s.game.red_star.status == False:
        p = [637,987]
        dirty_rects.append(screen.blit(star, p))
        s.game.coils.redROLamp.pulse(85)
        s.game.coils.yellowROLamp.pulse(85)
    if s.game.ball_return.position != 7:
        p = [380,945]
        dirty_rects.append(screen.blit(ball_return, p))
    pygame.display.update(dirty_rects)
    return

def animate_mixer4(s):
    global screen
    dirty_rects = []
    if s.game.right_special_card.status == False:
        p = [570,505]
        dirty_rects.append(screen.blit(special_card, p))
    if s.game.selection_feature_relay.status == False:
        p = [312,734]
        dirty_rects.append(screen.blit(super_selection, p))
    pygame.display.update(dirty_rects)
    return

def clear_features(s, num):
    global screen
    dirty_rects = []
    if s.game.before_fourth.status == False:
        dirty_rects.append(screen.blit(bg_gi, (7,695), pygame.Rect(7,695,91,66)))
    if s.game.before_fifth.status == False:
        dirty_rects.append(screen.blit(bg_gi, (624,695), pygame.Rect(624,695,91,66)))

    if s.game.selection_feature.position < 2:
        dirty_rects.append(screen.blit(bg_gi, (100,699), pygame.Rect(100,699,34,34)))
    if s.game.selection_feature.position < 3:
        dirty_rects.append(screen.blit(bg_gi, (140,699), pygame.Rect(140,699,34,34)))
    if s.game.selection_feature.position < 4:
        dirty_rects.append(screen.blit(bg_gi, (180,699), pygame.Rect(180,699,34,34)))
    if s.game.selection_feature.position < 6:
        dirty_rects.append(screen.blit(bg_gi, (215,694), pygame.Rect(215,694,39,39)))
        dirty_rects.append(screen.blit(bg_gi, (254,694), pygame.Rect(254,694,39,39)))
    if s.game.selection_feature.position < 7:
        dirty_rects.append(screen.blit(bg_gi, (293,694), pygame.Rect(293,694,39,39)))
    if s.game.selection_feature.position < 8:
        dirty_rects.append(screen.blit(bg_gi, (332,694), pygame.Rect(332,694,39,39)))
    if s.game.selection_feature.position < 9:
        dirty_rects.append(screen.blit(bg_gi, (372,694), pygame.Rect(372,694,39,39)))
    if s.game.selection_feature.position < 10:
        dirty_rects.append(screen.blit(bg_gi, (410,694), pygame.Rect(410,694,39,39)))
    if s.game.selection_feature.position < 11:
        dirty_rects.append(screen.blit(bg_gi, (451,694), pygame.Rect(451,694,39,39)))

    pygame.display.update(dirty_rects)

def draw_feature_animation(s, num):
    global screen
    dirty_rects = []

    if num in [4,15,10,21]:
        if s.game.before_fourth.status == False:
            p = [7,695]
            dirty_rects.append(screen.blit(before_fourth, p))
        if s.game.before_fifth.status == False and s.game.before_fourth.status == True:
            p = [624,695]
            dirty_rects.append(screen.blit(before_fourth, p))
        pygame.display.update(dirty_rects)
        return
   
    if num in [0,11,22]:
        if s.game.selection_feature.position < 2:
            p = [100,699]
            dirty_rects.append(screen.blit(s_arrow, p))
            pygame.display.update(dirty_rects)
            return
    if num in [9,20,23]:
        if s.game.selection_feature.position < 3:
            p = [140,699]
            dirty_rects.append(screen.blit(s_arrow, p))
            pygame.display.update(dirty_rects)
            return
    if num in [1,12,24]:
        if s.game.selection_feature.position < 4:
            p = [180,699]
            dirty_rects.append(screen.blit(s_arrow, p))
            pygame.display.update(dirty_rects)
            return
    if num in [2,13]:
        if s.game.selection_feature.position < 6:
            p = [215,694]
            dirty_rects.append(screen.blit(s_number, p))
            p = [254,694]
            dirty_rects.append(screen.blit(s_number, p))
            pygame.display.update(dirty_rects)
            return
    if num in [3,14,4,15]:
        if s.game.selection_feature.position < 7:
            p = [293,694]
            dirty_rects.append(screen.blit(s_number, p))
        pygame.display.update(dirty_rects)
        return
    if num in [5,16]:
        if s.game.selection_feature.position < 8:
            p = [332,694]
            dirty_rects.append(screen.blit(s_number, p))
        pygame.display.update(dirty_rects)
        return
    if num in [6,17]:
        if s.game.selection_feature.position < 9:
            p = [372,694]
            dirty_rects.append(screen.blit(s_number, p))
            pygame.display.update(dirty_rects)
            return
    if num in [7,18]:
        if s.game.selection_feature.position < 10:
            p = [410,694]
            dirty_rects.append(screen.blit(s_number, p))
            pygame.display.update(dirty_rects)
            return
    if num in [8,19]:
        if s.game.selection_feature.position < 11:
            p = [451,694]
            dirty_rects.append(screen.blit(s_number, p))
            pygame.display.update(dirty_rects)
            return
        
def feature_animation(args):
    global screen

    dirty_rects = []
    s = args[0]
    num = args[1]

    clear_features(s, num)

    draw_feature_animation(s, num)

def both_animation(args):
    global screen

    dirty_rects = []
    s = args[0]
    num = args[1]

    clear_features(s, num)
    clear_odds(s, num)

    if num % 2 == 0:
        clear_mixers(s)

    draw_odds_animation(s, num)
    draw_feature_animation(s, num)

