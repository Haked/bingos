#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
import procgame.game, sys, os
import procgame.config
import random
import procgame.sound

sys.path.insert(0,os.path.pardir)
import bingo_emulator.common.units as units
import bingo_emulator.common.functions as functions
from bingo_emulator.graphics import methods as graphics
from bingo_emulator.graphics.carnival_queen import *

class SinglecardBingo(procgame.game.Mode):
    def __init__(self, game):
        super(SinglecardBingo, self).__init__(game=game, priority=5)
        self.holes = []
        self.startup()
        self.game.sound.register_music('motor', "audio/six_card_motor.wav")
        self.game.sound.register_music('search', "audio/six_card_search_old.wav")
        self.game.sound.register_sound('add', "audio/six_card_add_card.wav")
        self.game.sound.register_sound('tilt', "audio/tilt.wav")
        self.game.sound.register_sound('step', "audio/step.wav")
        self.game.sound.register_sound('eb_search', "audio/EB_Search.wav")

    def sw_coin_active(self, sw):
        if self.game.eb_play.status == False:
            self.game.tilt.disengage()
            self.regular_play()
            self.scan_all()
        else:
            self.game.sound.stop('add')
            self.game.sound.play('add')
            self.game.cu = not self.game.cu
            self.game.spotting.spin()
            self.game.mixer1.spin()
            self.game.mixer2.spin()
            self.game.mixer3.spin()
            self.game.mixer4.spin()
            self.scan_eb()
            self.replay_step_down()
            self.game.reflex.decrease()

        self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_startButton_active(self, sw):
        self.game.eb_play.disengage()
        if self.game.replays > 0 or self.game.switches.freeplay.is_active():
            self.game.sound.stop('add')
            self.game.sound.play('add')
            self.game.tilt.disengage()
            self.regular_play()
            self.scan_all()
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_enter_active(self, sw):
        if self.game.switches.left.is_active() and self.game.switches.right.is_active():
            self.game.end_run_loop()
            os.system("/home/nbaldridge/proc/bingo_emulator/start_game.sh carnival_queen")
        else:
            if self.game.ball_count.position >= 4:
                self.game.sound.stop_music()
                if self.game.search_index.status == False:
                    self.game.sound.play('search')
                    self.search()


    def sw_trough4_active_for_1s(self, sw):
        if self.game.ball_count.position >= 4:
            self.timeout_actions()
    
    def timeout_actions(self):
        if (self.game.timer.position < 40):
            self.game.timer.step()
            self.delay(delay=5.0, handler=self.timeout_actions)
        else:
            self.tilt_actions()

    def sw_trough8_inactive_for_1ms(self, sw):
        if self.game.start.status == False:
            self.game.ball_count.position -= 1
            self.game.returned = True
            self.check_lifter_status()

    def sw_right_active(self, sw):
        if self.game.ball_count.position > 0:
            max_ball = 0
            if self.game.before_fourth.status == True:
                max_ball = 4
            elif self.game.before_fifth.status == True:
                max_ball = 5
            msu = self.game.magic_screen_feature.position

            if self.game.ball_count.position < max_ball:
                if self.game.magic_screen.position > 0:
                    self.game.magic_screen.stepdown()
                            
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_left_active(self, sw):
        if self.game.ball_count.position > 0:
            max_ball = 0
            if self.game.before_fourth.status == True:
                max_ball = 4
            elif self.game.before_fifth.status == True:
                max_ball = 5
            msu = self.game.magic_screen_feature.position
            if msu == 7:
                max_position = 4
            elif msu == 8:
                max_position = 5
            elif msu == 9:
                max_position = 6
            elif msu == 10:
                max_position = 7

            if self.game.ball_count.position < max_ball:
                if self.game.magic_screen.position < max_position:
                    self.game.magic_screen.step()
                            
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def check_shutter(self, start=0):
        if start == 1:
            if self.game.switches.smRunout.is_active():
                if self.game.switches.shutter.is_active():
                    self.game.coils.shutter.disable()
        else:
            if self.game.switches.shutter.is_inactive():
                if self.game.switches.smRunout.is_active():
                    self.game.coils.shutter.disable()


    def regular_play(self):
        self.cancel_delayed(name="search")
        self.cancel_delayed(name="lifter_status")
        self.cancel_delayed(name="card1_replay_step_up")
        self.game.search_index.disengage()
        self.game.coils.counter.pulse()

        self.game.cu = not self.game.cu
        self.game.spotting.spin()
        self.game.mixer1.spin()
        self.game.mixer2.spin()
        self.game.mixer3.spin()
        self.game.mixer4.spin()
        self.game.reflex.decrease()

        self.game.returned = False
        if self.game.start.status == True:
            if self.game.selector.position < 1:
                self.game.selector.step()
            if self.game.switches.shutter.is_inactive():
                self.game.coils.shutter.enable()
            self.replay_step_down()
            self.check_lifter_status()
        else:
            self.holes = []
            self.game.start.engage(self.game)
            self.game.coils.redROLamp.disable()
            self.game.coils.yellowROLamp.disable()
            self.game.red_replay_counter.reset()
            self.game.yellow_replay_counter.reset()
            self.game.green_replay_counter.reset()
            self.game.red_odds.reset()
            self.game.yellow_odds.reset()
            self.game.green_odds.reset()
            self.game.yellow_star.disengage()
            self.game.red_star.disengage()
            self.game.start.engage(self.game)
            self.game.selector.reset()
            self.game.ball_count.reset()
            self.game.extra_ball.reset()
            self.game.timer.reset()
            if self.game.magic_screen.position > 0:
                self.magic_screen_reset(self.game.magic_screen.position)
            self.game.magic_screen_feature.reset()
            self.game.before_fourth.disengage()
            self.game.before_fifth.disengage()
            self.game.red_super_section.disengage()
            self.game.yellow_super_section.disengage()
            self.game.three_blue.disengage()
            self.game.two_blue.disengage()
            self.game.three_blue.engage(self.game)
            
            self.game.sound.play_music('motor', -1)
            self.regular_play()
        self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
        self.game.tilt.disengage()

    def magic_screen_reset(self, number):
        if number > 0:
            self.game.magic_screen.stepdown()
            self.delay(name="display", delay=0, handler=graphics.carnival_queen.display, param=self)
            number -= 1
            self.delay(name="magic_screen_reset", delay=0.1, handler=self.magic_screen_reset, param=number)

    def check_lifter_status(self):
        if self.game.tilt.status == False:
            if self.game.switches.trough8.is_inactive() and self.game.switches.trough5.is_active() and self.game.switches.trough4.is_active() and self.game.switches.trough3.is_active() and self.game.switches.trough2.is_active():
                if self.game.switches.shooter.is_inactive():
                    self.game.coils.lifter.enable()
            else:
                if self.game.switches.trough4.is_active():
                    if self.game.switches.shooter.is_inactive():
                        if self.game.switches.gate.is_active():
                            self.game.coils.lifter.enable()
                else:
                    if self.game.switches.trough4.is_inactive():
                        if self.game.extra_ball.position >= 3 and self.game.ball_count.position <= 5:
                            if self.game.switches.shooter.is_inactive() and self.game.switches.trough3.is_active():
                                self.game.coils.lifter.enable()
                    if self.game.switches.trough3.is_inactive():
                        if self.game.extra_ball.position >= 6 and self.game.ball_count.position <= 6:
                            if self.game.switches.shooter.is_inactive() and self.game.switches.trough2.is_active():
                                self.game.coils.lifter.enable()
                    if self.game.switches.trough2.is_inactive() and self.game.ball_count.position <= 7:
                        if self.game.ball_count.position <= 7:
                            if self.game.extra_ball.position >= 9:
                                if self.game.switches.shooter.is_inactive():
                                    self.game.coils.lifter.enable()
                    if self.game.ball_count.position >= 8:
                        self.game.coils.lifter.disable()
                if self.game.returned == True and self.game.ball_count.position == 4:
                    if self.game.switches.shooter.is_inactive():
                        self.game.coils.lifter.enable()
                        self.game.returned = False
                if self.game.returned == True and self.game.ball_count.position == 8:
                    if self.game.switches.shooter.is_inactive():
                        self.game.coils.lifter.enable()
                        self.game.returned = False
        self.delay(name="lifter_status", delay=0, handler=self.check_lifter_status)

    def sw_smRunout_active_for_1ms(self, sw):
        if self.game.start.status == True:
            self.check_shutter(1)
        else:
            self.check_shutter()

    def sw_trough1_active(self, sw):
        if self.game.switches.shooter.is_active():
            self.game.coils.lifter.disable()

    def sw_shooter_active(self, sw):
        if self.game.ball_count.position == 7:
            self.game.coils.lifter.disable()
            self.cancel_delayed("lifter_status")

    def sw_ballLift_active_for_500ms(self, sw):
        if self.game.tilt.status == False:
            if self.game.switches.shooter.is_inactive():
                if self.game.ball_count.position < 5:
                    self.game.coils.lifter.enable()
                elif self.game.ball_count.position == 5 and self.game.extra_ball.position >= 3:
                    self.game.coils.lifter.enable()
                elif self.game.ball_count.position == 6 and self.game.extra_ball.position >= 6:
                    self.game.coils.lifter.enable()
                else:
                    if self.game.ball_count.position == 7 and self.game.extra_ball.position >= 9:
                        self.game.coils.lifter.enable()

    def sw_gate_inactive_for_1ms(self, sw):
        self.game.start.disengage()
        self.game.ball_count.step()
        if self.game.ball_count.position == 4 and self.game.before_fourth.status == True:
            self.game.before_fourth.disengage()
        if self.game.ball_count.position == 5 and self.game.before_fifth.status == True:
            self.game.before_fifth.disengage()
        if self.game.switches.shutter.is_active():
            self.game.coils.shutter.enable()
        if self.game.ball_count.position >= 5:
            self.game.coils.yellowROLamp.disable()
            self.game.coils.redROLamp.disable()
        self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)


    # This is really nasty, but it is how we render graphics for each individual hole.
    # numbers are added (or removed from) a list.  In this way, I can re-use the same
    # routine even for games where there are ball return functions like Surf Club.

    def sw_hole1_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(1)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole2_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(2)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole3_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(3)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole4_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(4)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole5_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(5)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole6_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(6)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole7_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(7)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole8_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(8)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole9_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(9)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole10_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(10)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole11_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(11)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole12_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(12)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole13_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(13)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole14_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(14)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole15_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(15)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole16_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(16)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole17_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(17)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole18_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(18)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole19_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(19)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole20_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(20)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole21_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(21)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole22_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(22)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole23_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(23)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole24_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(24)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_hole25_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(25)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_replayReset_active(self, sw):
        self.game.anti_cheat.disengage()
        self.holes = []
#        self.cancel_delayed(name="blink_title")
        graphics.carnival_queen.display(self)
        self.tilt_actions()
#        self.delay(name="blink_title", delay=1, handler=self.blink_title)
        self.replay_step_down(self.game.replays)

    def sw_redstar_active(self, sw):
        if self.game.red_star.status == True:
            if self.game.before_fifth.status == False:
                self.game.before_fifth.engage(self.game)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_yellowstar_active(self, sw):
        if self.game.yellow_star.status == True:
            if self.game.before_fifth.status == False:
                self.game.before_fifth.engage(self.game)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def tilt_actions(self):
        self.game.start.disengage()
        self.cancel_delayed(name="replay_reset")
        self.cancel_delayed(name="red_replay_step_up")
        self.cancel_delayed(name="yellow_replay_step_up")
        self.cancel_delayed(name="green_replay_step_up")
        self.game.coils.redROLamp.disable()
        self.game.coils.yellowROLamp.disable()
        self.game.search_index.disengage()
        if self.game.ball_count.position == 0:
            if self.game.switches.shutter.is_active():
                self.game.coils.shutter.enable()
        self.holes = []
        self.game.selector.reset()
        self.game.red_replay_counter.reset()
        self.game.yellow_replay_counter.reset()
        self.game.green_replay_counter.reset()
        self.game.yellow_star.disengage()
        self.game.red_star.disengage()
        self.game.magic_screen_feature.reset()
        self.game.red_super_section.disengage()
        self.game.yellow_super_section.disengage()
        self.game.before_fourth.disengage()
        self.game.before_fifth.disengage()
        self.game.three_blue.disengage()
        self.game.two_blue.disengage()
        self.game.ball_count.reset()
        self.game.red_odds.reset()
        self.game.yellow_odds.reset()
        self.game.green_odds.reset()
        self.game.eb_play.disengage()
        self.game.extra_ball.reset()
        self.game.anti_cheat.engage(game)
        self.game.tilt.engage(self.game)
        self.game.sound.stop_music()
        self.game.sound.play('tilt')
        # displays "Tilt" on the backglass, you have to recoin.
        self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def sw_tilt_active(self, sw):
        if self.game.tilt.status == False:
            self.tilt_actions()

    def replay_step_down(self, number=0):
        if number > 0:
            if number > 1:
                self.game.replays -= 1
                graphics.replay_step_down(self.game.replays, graphics.carnival_queen.reel1, graphics.carnival_queen.reel10, graphics.carnival_queen.reel100)
                self.game.coils.registerDown.pulse()
                number -= 1
                self.delay(name="display", delay=0, handler=graphics.carnival_queen.display, param=self)
                self.delay(name="replay_reset", delay=0.0, handler=self.replay_step_down, param=number)
            elif number == 1:
                self.game.replays -= 1
                graphics.replay_step_down(self.game.replays, graphics.carnival_queen.reel1, graphics.carnival_queen.reel10, graphics.carnival_queen.reel100)
                self.game.coils.registerDown.pulse()
                number -= 1
                self.delay(name="display", delay=0, handler=graphics.carnival_queen.display, param=self)
                self.cancel_delayed(name="replay_reset")
        else: 
            if self.game.replays > 0:
                self.game.replays -= 1
                graphics.replay_step_down(self.game.replays, graphics.carnival_queen.reel1, graphics.carnival_queen.reel10, graphics.carnival_queen.reel100)
                self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
            self.game.coils.registerDown.pulse()

    def replay_step_up(self):
        if self.game.replays < 899:
            self.game.replays += 1
            graphics.replay_step_up(self.game.replays, graphics.carnival_queen.reel1, graphics.carnival_queen.reel10, graphics.carnival_queen.reel100)
        self.game.coils.registerUp.pulse()
        self.game.reflex.increase()
        graphics.carnival_queen.display(self)

    def sw_yellow_active(self, sw):
        if self.game.ball_count.position >= 4:
            if self.game.eb_play.status == False:
                self.game.spotting.spin()
                self.game.mixer1.spin()
                self.game.mixer2.spin()
                self.game.mixer3.spin()
                self.game.mixer4.spin()
                self.game.eb_play.engage(self.game)
                self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
                self.sw_yellow_active(sw)
            if self.game.eb_play.status == True and (self.game.replays > 0 or self.game.switches.freeplay.is_active()):
                self.game.sound.stop('add')
                self.game.sound.play('add')
                self.game.cu = not self.game.cu
                self.game.spotting.spin()
                self.game.mixer1.spin()
                self.game.mixer2.spin()
                self.game.mixer3.spin()
                self.game.mixer4.spin()
                self.scan_eb()
                self.replay_step_down()
                self.game.reflex.decrease()
                self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
            
    #OK - here's the deal: Magic Screen games' search sequence is INCREDIBLY
    #complex compared to the prior games.  There are not only multiple sets
    #of odds, but also the game has to account for the position of the screen
    #the sequence unit, and the winner unit, along with any other special
    #cases like the yellow or red super section.
    #
    #In the real games, the search relays are triggered out of sequence, and
    #the winner/sequence unit is stepped as necessary, until the unit steps
    #a certain number of times.  In THIS game, I don't necessarily have to
    #worry about the position of the search relays if the section scoring
    #is engaged.  So I probably won't.  

    #### FINISH THIS


    def search(self):
        # The search workflow/logic will determine if you actually have a winner, but it is a bit tricky.
        # if the ball is in a particular hole, the search relays need to click and/or clack, and 
        # when you have at least three going at once, it should latch on the search index and score.
        # This scoring is tempered by the selector disc.  You have to have the card enabled that you're
        # winning on.  This whole process will have to happen on a rotational basis.  The search should really
        # begin immediately upon the first ball landing in the hole.
        # I suspect that the best, fastest way to complete the search is actually to reimplement the mechanical
        # search activity.  For each revolution of the search disc (which happens about every 5-7 seconds), the
        # game will activate() each search relay for each 'hot' rivet on the search disc.  This can be on a different
        # wiper finger for each set of rivets on the search disc.
#        self.cancel_delayed(name="blink_title")
        self.game.sound.stop_music()
        self.game.sound.play_music('search', -1)
       
        if self.game.magic_screen.position <= 4:
            for i in range(0, 13):
                self.r = self.closed_search_relays(self.game.searchdisc.position)
                self.game.searchdisc.spin()
                self.wipers = self.r[0]
                self.red = self.r[1]
                self.yellow = self.r[2]
                self.green = self.r[3]
                self.blue = False

                # From here, I need to determine based on the value of r, whether to latch the search index and score. 
                # I need to determine the best winner on each card.  To do this, I must compare the position of the replay counter before
                # determining the winner. Reminder that my replay counters are a 1:1 representation.

                self.match = []
                for key in self.wipers:
                    for number in self.holes:
                        if number == key:
                            self.match.append(self.wipers[key])
                            relays = sorted(set(self.match))
                            #TODO Play sound for each relay closure.
                            s = functions.count_seq(relays)
                            if s >= 3:
                                self.find_winner(s, self.red, self.yellow, self.green, self.blue)
                                break
                            
        if self.game.magic_screen.position >= 1:
            self.r = self.find_section_winners()
            self.red = self.r[0]
            self.yellow = self.r[1]
            self.green = self.r[2]
            self.blue = self.r[3]
            self.red_winner = self.r[4]
            self.yellow_winner = self.r[5]
            self.green_winner = self.r[6]
            self.blue_winner = self.r[7]
            self.red_ss_winner = self.r[8]
            self.yellow_ss_winner = self.r[9]
            self.big_green_winner = self.r[10]
            self.small_green_winner = self.r[11]
            self.top_red_winner = self.r[12]
            self.bottom_yellow_winner = self.r[13]

            self.find_winner(0, self.red, self.yellow, self.green, self.blue, self.red_winner, self.yellow_winner, self.green_winner, self.blue_winner, self.red_ss_winner, self.yellow_ss_winner, self.big_green_winner, self.small_green_winner, self.top_red_winner, self.bottom_yellow_winner)
    #        self.delay(name="blink_title", delay=3, handler=self.blink_title)

    # THIS NEEDS TO BE CALLED IF THE SCREEN IF OUT OF INDEX POSITION

    def find_section_winners(self):
        self.red_winner = 0
        self.yellow_winner = 0
        self.green_winner = 0
        self.blue_winner = 0
        self.red = False
        self.yellow = False
        self.green = False
        self.blue = False
        self.red_ss_winner = 0
        self.yellow_ss_winner = 0
        self.big_green_winner = 0
        self.small_green_winner = 0
        self.top_red_winner = 0
        self.bottom_yellow_winner = 0

        #Position 'A'
        if self.game.magic_screen.position == 1:
            if 15 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 18 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 17 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True

            if 20 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 10 in self.holes:
                self.red_ss_winner += 1
                self.red = True

        #Position 'B'
        if self.game.magic_screen.position == 2:
            if 15 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 11 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 22 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 13 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True

            if 10 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 3 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 21 in self.holes:
                self.red_ss_winner += 1
                self.red = True

            if 18 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 17 in self.holes:
                self.big_green_winner += 1
            if 20 in self.holes:
                self.big_green_winner += 1
                self.green = True

        #Position 'C'
        if self.game.magic_screen.position == 3:
            if 15 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 11 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 2 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 7 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 16 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True

            if 10 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 3 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 14 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 5 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 20 in self.holes:
                self.red_ss_winner += 1
                self.red = True

            if 22 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 13 in self.holes:
                self.big_green_winner += 1
            if 21 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 17 in self.holes:
                self.big_green_winner += 1
                self.green = True
            
            if 18 in self.holes:
                self.top_red_winner += 1
                self.red = True

        #Position 'D'
        if self.game.magic_screen.position == 4:
            if 1 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 11 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 2 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 19 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 24 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True

            if 23 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 8 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 14 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 3 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 21 in self.holes:
                self.red_ss_winner += 1
                self.red = True

            if 7 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 16 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 5 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 13 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 17 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 20 in self.holes:
                self.big_green_winner += 1
                self.green = True
            
            if 18 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 15 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 22 in self.holes:
                self.top_red_winner += 1
                self.red = True

            if 3 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True

        #Position 'E'
        if self.game.magic_screen.position == 5:
            if 9 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 4 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 25 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 1 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 2 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True

            if 6 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 12 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 8 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 14 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 5 in self.holes:
                self.red_ss_winner += 1
                self.red = True

            if 19 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 24 in self.holes:
                self.big_green_winner += 1
            if 23 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 16 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 13 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 21 in self.holes:
                self.big_green_winner += 1
                self.green = True
            
            if 7 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 22 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 11 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 15 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 18 in self.holes:
                self.top_red_winner += 1
                self.red = True

            if 3 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            if 10 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            if 20 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True

            if 17 in self.holes:
                self.blue_winner += 1
                self.blue = True

        #Position 'F'
        if self.game.magic_screen.position == 6:
            if 9 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True
            if 1 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True

            if 12 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 8 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 23 in self.holes:
                self.red_ss_winner += 1
                self.red = True

            if 4 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 25 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 6 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 24 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 16 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 5 in self.holes:
                self.big_green_winner += 1
                self.green = True
            
            if 19 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 7 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 2 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 22 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 11 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 18 in self.holes:
                self.top_red_winner += 1
                self.red = True

            if 15 in self.holes:
                self.small_green_winner += 1
                self.green = True

            if 14 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            if 3 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            if 21 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            if 10 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            
            if 13 in self.holes:
                self.blue_winner += 1
                self.blue = True
            if 17 in self.holes:
                self.blue_winner += 1
                self.blue = True
            if 20 in self.holes:
                self.blue_winner += 1
                self.blue = True
                
        #Position 'G'
        if self.game.magic_screen.position == 7:
            if 9 in self.holes:
                self.yellow_ss_winner += 1
                self.yellow = True

            if 12 in self.holes:
                self.red_ss_winner += 1
                self.red = True
            if 6 in self.holes:
                self.red_ss_winner += 1
                self.red = True

            if 24 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 25 in self.holes:
                self.big_green_winner += 1
                self.green = True
            if 23 in self.holes:
                self.big_green_winner += 1
                self.green = True
            
            if 4 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 1 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 19 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 2 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 7 in self.holes:
                self.top_red_winner += 1
                self.red = True
            if 22 in self.holes:
                self.top_red_winner += 1
                self.red = True

            if 11 in self.holes:
                self.small_green_winner += 1
                self.green = True
            if 15 in self.holes:
                self.small_green_winner += 1
                self.green = True
            if 18 in self.holes:
                self.small_green_winner += 1
                self.green = True
            if 17 in self.holes:
                self.small_green_winner += 1
                self.green = True

            if 8 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            if 14 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            if 5 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            if 3 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            if 10 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            if 20 in self.holes:
                self.bottom_yellow_winner += 1
                self.yellow = True
            
            if 13 in self.holes:
                self.blue_winner += 1
                self.blue = True
            if 16 in self.holes:
                self.blue_winner += 1
                self.blue = True
            if 21 in self.holes:
                self.blue_winner += 1
                self.blue = True

        return (self.red, self.yellow, self.green, self.blue, self.red_winner, self.yellow_winner, self.green_winner, self.blue_winner, self.red_ss_winner, self.yellow_ss_winner, self.big_green_winner, self.small_green_winner, self.top_red_winner, self.bottom_yellow_winner)


    def find_winner(self, relays, red, yellow, green, blue, red_winner=0, yellow_winner=0, green_winner=0, blue_winner=0, red_ss_winner=0, yellow_ss_winner=0, big_green_winner=0, small_green_winner=0, top_red_winner=0, bottom_yellow_winner=0):
        if self.game.search_index.status == False and self.game.replays < 899:
            if self.game.red_odds.position == 1:
                redthreeodds = 4
                redfourodds = 16
                redfiveodds = 75
            elif self.game.red_odds.position == 2:
                redthreeodds = 6
                redfourodds = 20
                redfiveodds = 75
            elif self.game.red_odds.position == 3:
                redthreeodds = 8
                redfourodds = 24
                redfiveodds = 96
            elif self.game.red_odds.position == 4:
                redthreeodds = 16
                redfourodds = 50
                redfiveodds = 96
            elif self.game.red_odds.position == 5:
                redthreeodds = 32
                redfourodds = 96
                redfiveodds = 200
            elif self.game.red_odds.position == 6:
                redthreeodds = 64
                redfourodds = 144
                redfiveodds = 300
            elif self.game.red_odds.position == 7:
                redthreeodds = 120
                redfourodds = 240
                redfiveodds = 450
            elif self.game.red_odds.position == 8:
                redthreeodds = 192
                redfourodds = 480
                redfiveodds = 600
            if self.game.yellow_odds.position == 1:
                yellowthreeodds = 4
                yellowfourodds = 16
                yellowfiveodds = 75
            elif self.game.yellow_odds.position == 2:
                yellowthreeodds = 6
                yellowfourodds = 20
                yellowfiveodds = 75
            elif self.game.yellow_odds.position == 3:
                yellowthreeodds = 8
                yellowfourodds = 24
                yellowfiveodds = 96
            elif self.game.yellow_odds.position == 4:
                yellowthreeodds = 16
                yellowfourodds = 50
                yellowfiveodds = 96
            elif self.game.yellow_odds.position == 5:
                yellowthreeodds = 32
                yellowfourodds = 96
                yellowfiveodds = 200
            elif self.game.yellow_odds.position == 6:
                yellowthreeodds = 64
                yellowfourodds = 144
                yellowfiveodds = 300
            elif self.game.yellow_odds.position == 7:
                yellowthreeodds = 120
                yellowfourodds = 240
                yellowfiveodds = 450
            elif self.game.yellow_odds.position == 8:
                yellowthreeodds = 192
                yellowfourodds = 480
                yellowfiveodds = 600
            if self.game.green_odds.position == 1:
                greenthreeodds = 4
                greenfourodds = 16
                greenfiveodds = 75
            elif self.game.green_odds.position == 2:
                greenthreeodds = 6
                greenfourodds = 20
                greenfiveodds = 75
            elif self.game.green_odds.position == 3:
                greenthreeodds = 8
                greenfourodds = 24
                greenfiveodds = 96
            elif self.game.green_odds.position == 4:
                greenthreeodds = 16
                greenfourodds = 50
                greenfiveodds = 96
            elif self.game.green_odds.position == 5:
                greenthreeodds = 32
                greenfourodds = 96
                greenfiveodds = 200
            elif self.game.green_odds.position == 6:
                greenthreeodds = 64
                greenfourodds = 144
                greenfiveodds = 300
            elif self.game.green_odds.position == 7:
                greenthreeodds = 120
                greenfourodds = 240
                greenfiveodds = 450
            elif self.game.green_odds.position == 8:
                greenthreeodds = 192
                greenfourodds = 480
                greenfiveodds = 600



            if red_ss_winner == 2 or yellow_ss_winner == 2 or blue_winner == 2:
                if self.game.red_super_section.status == True:
                    if red_ss_winner == 2:
                        if self.game.search_index.status == False:
                            if self.game.red_replay_counter.position < redthreeodds:
                                self.game.search_index.engage(self.game)
                                self.red_replay_step_up(redthreeodds - self.game.red_replay_counter.position)
                if self.game.yellow_super_section.status == True:
                    if yellow_ss_winner == 2:
                        if self.game.search_index.status == False:
                            if self.game.yellow_replay_counter.position < yellowthreeodds:
                                self.game.search_index.engage(self.game)
                                self.yellow_replay_step_up(yellowthreeodds - self.game.yellow_replay_counter.position)
                if self.game.two_blue.status == True:
                    if blue_winner == 2:
                        print "HERE"
                        if self.game.search_index.status == False:
                            print "NOT STUCK IN SEARCH"
                            if self.game.green_replay_counter.position < greenfiveodds:
                                print greenfiveodds
                                self.game.search_index.engage(self.game)
                                print "NOW STUCK"
                                self.green_replay_step_up(greenfiveodds - self.game.green_replay_counter.position)
            if relays == 3 or red_winner == 3 or yellow_winner == 3 or green_winner == 3 or red_ss_winner == 3 or yellow_ss_winner == 3 or blue_winner == 3 or big_green_winner == 3 or small_green_winner == 3 or top_red_winner == 3 or bottom_yellow_winner == 3:
                    if red_ss_winner == 3:
                        if self.game.search_index.status == False:
                            if self.game.red_super_section.status == True:
                                if self.game.red_replay_counter.position < redfourodds:
                                    self.game.search_index.engage(self.game)
                                    self.red_replay_step_up(redfourodds - self.game.red_replay_counter.position)
                            else:
                                if self.game.red_replay_counter.position < redthreeodds:
                                    self.game.search_index.engage(self.game)
                                    self.red_replay_step_up(redthreeodds - self.game.red_replay_counter.position)
                    if yellow_ss_winner == 3:
                        if self.game.search_index.status == False:
                            if self.game.yellow_super_section.status == True:
                                if self.game.yellow_replay_counter.position < yellowfourodds:
                                    self.game.search_index.engage(self.game)
                                    self.yellow_replay_step_up(yellowfourodds - self.game.yellow_replay_counter.position)
                            else:
                                if self.game.yellow_replay_counter.position < yellowthreeodds:
                                    self.game.search_index.engage(self.game)
                                    self.yellow_replay_step_up(yellowthreeodds - self.game.yellow_replay_counter.position)
                    if (red == 1 and relays == 3) or top_red_winner == 3:
                        if self.game.search_index.status == False:
                            if self.game.red_replay_counter.position < redthreeodds:
                                self.game.search_index.engage(self.game)
                                self.red_replay_step_up(redthreeodds - self.game.red_replay_counter.position)
                    if (yellow == 1 and relays == 3) or bottom_yellow_winner == 3:
                        if self.game.search_index.status == False:
                            if self.game.yellow_replay_counter.position < yellowthreeodds:
                                self.game.search_index.engage(self.game)
                                self.yellow_replay_step_up(yellowthreeodds - self.game.yellow_replay_counter.position)
                    if (green == 1 and relays == 3) or big_green_winner == 3 or small_green_winner == 3:
                        if self.game.search_index.status == False:
                            if self.game.green_replay_counter.position < greenthreeodds:
                                self.game.search_index.engage(self.game)
                                self.green_replay_step_up(greenthreeodds - self.game.green_replay_counter.position)
                    if blue_winner == 3:
                        print "HERE"
                        if self.game.search_index.status == False:
                            print "NOT STUCK IN SEARCH"
                            if self.game.green_replay_counter.position < greenfiveodds:
                                print greenfiveodds
                                self.game.search_index.engage(self.game)
                                print "NOW STUCK"
                                self.green_replay_step_up(greenfiveodds - self.game.green_replay_counter.position)
            if relays == 4 or red_winner == 4 or yellow_winner == 4 or green_winner == 4 or red_ss_winner == 4 or yellow_ss_winner == 4 or big_green_winner == 4 or small_green_winner == 4 or top_red_winner == 4 or bottom_yellow_winner == 4:
                    if red_ss_winner == 4:
                        if self.game.search_index.status == False:
                            if self.game.red_super_section.status == True:
                                if self.game.red_replay_counter.position < redfiveodds:
                                    self.game.search_index.engage(self.game)
                                    self.red_replay_step_up(redfiveodds - self.game.red_replay_counter.position)
                            else:
                                if self.game.red_replay_counter.position < redfourodds:
                                    self.game.search_index.engage(self.game)
                                    self.red_replay_step_up(redfourodds - self.game.red_replay_counter.position)
                    if yellow_ss_winner == 4:
                        if self.game.search_index.status == False:
                            if self.game.yellow_super_section.status == True:
                                if self.game.yellow_replay_counter.position < yellowfiveodds:
                                    self.game.search_index.engage(self.game)
                                    self.yellow_replay_step_up(yellowfiveodds - self.game.yellow_replay_counter.position)
                            else:
                                if self.game.yellow_replay_counter.position < yellowfourodds:
                                    self.game.search_index.engage(self.game)
                                    self.yellow_replay_step_up(yellowfourodds - self.game.yellow_replay_counter.position)
                    if (red == 1 and relays == 4) or top_red_winner == 4:
                        if self.game.search_index.status == False:
                            if self.game.red_replay_counter.position < redfourodds:
                                self.game.search_index.engage(self.game)
                                self.red_replay_step_up(redfourodds - self.game.red_replay_counter.position)
                    if (yellow == 1 and relays == 4) or bottom_yellow_winner == 4:
                        if self.game.search_index.status == False:
                            if self.game.yellow_replay_counter.position < yellowfourodds:
                                self.game.search_index.engage(self.game)
                                self.yellow_replay_step_up(yellowfourodds - self.game.yellow_replay_counter.position)
                    if (green == 1 and relays == 4) or big_green_winner == 4 or small_green_winner == 4:
                        if self.game.search_index.status == False:
                            if self.game.green_replay_counter.position < greenfourodds:
                                self.game.search_index.engage(self.game)
                                self.green_replay_step_up(greenfourodds - self.game.green_replay_counter.position)
            if relays == 5 or red_winner == 5 or yellow_winner == 5 or green_winner == 5 or red_ss_winner == 5 or yellow_ss_winner == 5 or big_green_winner == 5 or small_green_winner == 5 or top_red_winner == 5 or bottom_yellow_winner == 5:
                if (red == 1 and relays == 5) or red_ss_winner == 5 or top_red_winner == 5:
                    if self.game.search_index.status == False:
                        if self.game.red_replay_counter.position < redfiveodds:
                            self.game.search_index.engage(self.game)
                            self.red_replay_step_up(redfiveodds - self.game.red_replay_counter.position)
                if (yellow == 1 and relays == 5) or yellow_ss_winner == 5 or bottom_yellow_winner == 5:
                    if self.game.search_index.status == False:
                        if self.game.yellow_replay_counter.position < yellowfiveodds:
                            self.game.search_index.engage(self.game)
                            self.yellow_replay_step_up(yellowfiveodds - self.game.yellow_replay_counter.position)
                if (green == 1 and relays == 5) or big_green_winner == 5 or small_green_winner == 5:
                    if self.game.search_index.status == False:
                        if self.game.green_replay_counter.position < greenfiveodds:
                            self.game.search_index.engage(self.game)
                            self.green_replay_step_up(greenfiveodds - self.game.green_replay_counter.position)


    def red_replay_step_up(self, number):
        if number >= 1:
            self.game.red_replay_counter.step()
            number -= 1
            self.replay_step_up()
            if self.game.replays == 899:
                number = 0
            self.delay(name="red_replay_step_up", delay=0.1, handler=self.red_replay_step_up, param=number)
        else:
            self.game.search_index.disengage()
            self.cancel_delayed(name="red_replay_step_up")
            self.search()
            
    def yellow_replay_step_up(self, number):
        if number >= 1:
            self.game.yellow_replay_counter.step()
            number -= 1
            self.replay_step_up()
            if self.game.replays == 899:
                number = 0
            self.delay(name="yellow_replay_step_up", delay=0.1, handler=self.yellow_replay_step_up, param=number)
        else:
            self.game.search_index.disengage()
            self.cancel_delayed(name="yellow_replay_step_up")
            self.search()

    def green_replay_step_up(self, number):
        if number >= 1:
            self.game.green_replay_counter.step()
            number -= 1
            self.replay_step_up()
            if self.game.replays == 899:
                number = 0
            self.delay(name="green_replay_step_up", delay=0.1, handler=self.green_replay_step_up, param=number)
        else:
            self.game.search_index.disengage()
            self.cancel_delayed(name="green_replay_step_up")
            self.search()


    def closed_search_relays(self, rivets):
        # This function is critical, as it will determine which card is returned, etc.  I need to check the position of the
        # replay counter for the card. We will get a row back
        # that has the numbers on the position which will return the search relay connected.  When three out of the five relays
        # are connected, we get a winner!

        # I have to adjust this quite a bit for magic screen games.  I will implement the standard search relays based on
        # what I decide (commented) because the search logic is insanely complex in the real deal.  It will be easier
        # for non-section wins to search based on what I enter here.

        # For section wins, see find_section_winner() further into the code.
        
        self.pos = {}
        red = False
        yellow = False
        green = False

        if self.game.magic_screen.position == 0:
            # Basic Position
            self.pos[0] = {}
            
            # Red Winners
            # Top row Horizontal
            self.pos[1] = {9:1, 1:2, 2:3, 11:4, 15:5}
            # fourth row horiz
            self.pos[2] = {6:1, 23:2, 5:3, 21:4, 20:5}
            # second column
            self.pos[3] = {1:1, 19:2, 24:3, 23:4, 8:5}
            # fifth column
            self.pos[4] = {15:1, 18:2, 17:3, 20:4, 10:5}

            # Yellow Winners
            # 2 row
            self.pos[5] = {4:1, 19:2, 7:3, 22:4, 18:5}
            # 5 row
            self.pos[6] = {12:1, 8:2, 14:3, 3:4, 10:5}
            # 1 column
            self.pos[7] = {9:1, 4:2, 25:3, 6:4, 12:5}
            # 4 column
            self.pos[8] = {11:1, 22:2, 13:3, 21:4, 3:5}

            # Green Winners
            # 3 row
            self.pos[9] = {25:1, 24:2, 16:3, 13:4, 17:5}
            # 3 column
            self.pos[10] = {2:1, 7:2, 16:3, 5:4, 14:5}
            # 1st diag
            self.pos[11] = {9:1, 19:2, 16:3, 21:4, 10:5}
            # 2nd diag
            self.pos[12] = {15:1, 22:2, 16:3, 23:4, 12:5}


            if rivets == 1 or rivets == 2 or rivets == 3 or rivets == 4:
                red = True
            if rivets == 5 or rivets == 6 or rivets == 7 or rivets == 8:
                yellow = True
            if rivets == 9 or rivets == 10 or rivets == 11 or rivets == 12:
                green = True
                
            return (self.pos[rivets], red, yellow, green)

        elif self.game.magic_screen.position == 1:
            # "A" Position
            self.pos[0] = {}
            
            # Red Winners
            # Top row Horizontal
            self.pos[1] = {9:1, 1:2, 2:3, 11:4}
            # fourth row horiz
            self.pos[2] = {6:1, 23:2, 5:3, 21:4}
            # second column
            self.pos[3] = {9:1, 4:2, 25:3, 6:4, 12:5}
            # fifth column
            self.pos[4] = {11:1, 22:2, 13:3, 21:4, 3:5}

            # Yellow Winners
            # 2 row
            self.pos[5] = {4:1, 19:2, 7:3, 22:4}
            # 5 row
            self.pos[6] = {12:1, 8:2, 14:3, 3:4}
            # 1 column
            self.pos[7] = {}
            # 4 column
            self.pos[8] = {2:1, 7:2, 16:3, 5:4, 14:5}

            # Green Winners
            # 3 row
            self.pos[9] = {25:1, 24:2, 16:3, 13:4}
            # 3 column
            self.pos[10] = {1:1, 19:2, 24:3, 23:4, 8:5}
            # 1st diag
            self.pos[11] = {4:1, 24:2, 5:3, 3:4}
            # 2nd diag
            self.pos[12] = {6:1, 24:2, 7:3, 11:4}


            if rivets == 1 or rivets == 2 or rivets == 3 or rivets == 4:
                red = True
            if rivets == 5 or rivets == 6 or rivets == 7 or rivets == 8:
                yellow = True
            if rivets == 9 or rivets == 10 or rivets == 11 or rivets == 12:
                green = True
                
            return (self.pos[rivets], red, yellow, green)

        elif self.game.magic_screen.position == 2:
            # "B" Position
            self.pos[0] = {}
            
            # Red Winners
            # Top row Horizontal
            self.pos[1] = {9:1, 1:2, 2:3}
            # fourth row horiz
            self.pos[2] = {6:1, 23:2, 5:3}
            # second column
            self.pos[3] = {}
            # fifth column
            self.pos[4] = {2:1, 7:2, 16:3, 5:4, 14:5}

            # Yellow Winners
            # 2 row
            self.pos[5] = {4:1, 19:2, 7:3}
            # 5 row
            self.pos[6] = {12:1, 8:2, 14:3}
            # 1 column
            self.pos[7] = {}
            # 4 column
            self.pos[8] = {1:1, 19:2, 24:3, 23:4, 8:5}

            # Green Winners
            # 3 row
            self.pos[9] = {25:1, 24:2, 16:3}
            # 3 column
            self.pos[10] = {9:1, 4:2, 25:3, 6:4, 12:5}
            # 1st diag
            self.pos[11] = {25:1, 23:2, 14:3}
            # 2nd diag
            self.pos[12] = {25:1, 19:2, 2:3}


            if rivets == 1 or rivets == 2 or rivets == 3 or rivets == 4:
                red = True
            if rivets == 5 or rivets == 6 or rivets == 7 or rivets == 8:
                yellow = True
            if rivets == 9 or rivets == 10 or rivets == 11 or rivets == 12:
                green = True
                
            return (self.pos[rivets], red, yellow, green)

        elif self.game.magic_screen.position == 3:
            # "C" Position
            self.pos[0] = {}
            
            # Red Winners
            # Top row Horizontal
            self.pos[1] = {}
            # fourth row horiz
            self.pos[2] = {}
            # second column
            self.pos[3] = {}
            # fifth column
            self.pos[4] = {1:1, 19:2, 24:3, 23:4, 8:5}

            # Yellow Winners
            # 2 row
            self.pos[5] = {}
            # 5 row
            self.pos[6] = {}
            # 1 column
            self.pos[7] = {}
            # 4 column
            self.pos[8] = {9:1, 4:2, 25:3, 6:4, 12:5}

            # Green Winners
            # 3 row
            self.pos[9] = {}
            # 3 column
            self.pos[10] = {}
            # 1st diag
            self.pos[11] = {}
            # 2nd diag
            self.pos[12] = {}


            if rivets == 1 or rivets == 2 or rivets == 3 or rivets == 4:
                red = True
            if rivets == 5 or rivets == 6 or rivets == 7 or rivets == 8:
                yellow = True
            if rivets == 9 or rivets == 10 or rivets == 11 or rivets == 12:
                green = True
                
            return (self.pos[rivets], red, yellow, green)

        elif self.game.magic_screen.position == 4:
            # "D" Position
            self.pos[0] = {}
            
            # Red Winners
            # Top row Horizontal
            self.pos[1] = {}
            # fourth row horiz
            self.pos[2] = {}
            # second column
            self.pos[3] = {}
            # fifth column
            self.pos[4] = {9:1, 4:2, 25:3, 6:4, 12:5}

            # Yellow Winners
            # 2 row
            self.pos[5] = {}
            # 5 row
            self.pos[6] = {}
            # 1 column
            self.pos[7] = {}
            # 4 column
            self.pos[8] = {}

            # Green Winners
            # 3 row
            self.pos[9] = {}
            # 3 column
            self.pos[10] = {}
            # 1st diag
            self.pos[11] = {}
            # 2nd diag
            self.pos[12] = {}


            if rivets == 1 or rivets == 2 or rivets == 3 or rivets == 4:
                red = True
            if rivets == 5 or rivets == 6 or rivets == 7 or rivets == 8:
                yellow = True
            if rivets == 9 or rivets == 10 or rivets == 11 or rivets == 12:
                green = True
                
            return (self.pos[rivets], red, yellow, green)

        # No other positions have in-line winners.  Check the sections instead.

    
    def scan_all(self):
        #Animate scanning of everything - this happens through the spotting disc
        self.all_probability()

    def all_probability(self):
        #Hooray!  Mixer1 is documented on Phil's site!  This is correct per the schematic and diagrams.
        mix1 = self.game.mixer1.connected_rivet()
        if self.game.reflex.connected_rivet() == 0:
            #Worst position for reflex - requires mixer1 to be in the three liberal positions for the connection of the wires bypassing the reflex.
            if (mix1 != 17 or mix1 != 1 or mix1 != 10 or mix1 != 19 or mix1 != 4 or mix1 != 9 or mix1 != 23 or mix1 != 2 or mix1 != 7 or mix1 != 21):
                self.scan_odds()
                self.scan_features()
        if self.game.reflex.connected_rivet() == 1 and (mix1 != 17 or mix1 != 1 or mix1 != 10 or mix1 != 19 or mix1 != 4 or mix1 != 9 or mix1 != 23):
            self.scan_odds()
            self.scan_features()
        elif self.game.reflex.connected_rivet() == 2 and (mix1 != 17 or mix1 != 1 or mix1 != 10 or mix1 != 19):
            self.scan_odds()
            self.scan_features()
        elif self.game.reflex.connected_rivet() == 3 and (mix1 != 17):
            self.scan_odds()
            self.scan_features()
        elif self.game.reflex.connected_rivet() == 4:
            self.scan_odds()
            self.scan_features()
        else:
            s = random.randint(1,8)
            self.animate_odds_scan(s)
            s = random.randint(1,4)
            self.animate_feature_scan(s)
            if self.game.yellow_odds.position == 0:
                self.game.yellow_odds.step()
            if self.game.red_odds.position == 0:
                self.game.red_odds.step()
            if self.game.green_odds.position == 0:
                self.game.green_odds.step()

    def scan_odds(self):
        if self.game.yellow_odds.position <= 1:
            self.game.yellow_odds.step()
        if self.game.red_odds.position <= 1:
            self.game.red_odds.step()
        if self.game.green_odds.position <= 1:
            self.game.green_odds.step()
        if self.game.yellow_odds.position >= 2 and self.game.red_odds.position >= 2 and self.game.green_odds.position >= 2:
            s = random.randint(1,8)
            self.animate_odds_scan(s)
            p = self.red_odds_probability()
            if p == 1:
                es = self.check_extra_step()
                if es == 1:
                    i = random.randint(1,6)
                    if self.game.red_super_section.status == False:
                        self.red_extra_step(i)
                    else:
                        self.yellow_extra_step(i)
                else:
                    self.game.red_odds.step()
            p = self.yellow_odds_probability()
            if p == 1:
                es = self.check_extra_step()
                if es == 1:
                    i = random.randint(1,6)
                    if self.game.yellow_super_section.status == False:
                        self.yellow_extra_step(i)
                    else:
                        self.red_extra_step(i)
                else:
                    self.game.yellow_odds.step()
            p = self.green_odds_probability()
            if p == 1:
                self.game.green_odds.step()

    def red_extra_step(self, number):
        if number > 0:
            self.game.red_odds.step()
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
            number -= 1
            self.delay(name="extra_step", delay=0.1, handler=self.red_extra_step, param=number)

    def yellow_extra_step(self, number):
        if number > 0:
            self.game.yellow_odds.step()
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
            number -= 1
            self.delay(name="extra_step", delay=0.1, handler=self.yellow_extra_step, param=number)

    def check_extra_step(self):
        i = random.randint(0,32)
        if i == 16:
            return 1
        else:
            return 0

    def red_odds_probability(self):
        # Check position of Mixer 4, and Mixer 3 and current 
        # position of the odds, along with trip relays.
        # For first check, guaranteed double stepup.  Probability doesn't 
        # factor, so I will return as part of the initial check above.
        if self.game.before_fifth.status == True:
            mix4 = self.game.mixer4.position
            if mix4 == 3 or mix4 == 5 or mix4 == 7 or mix4 == 11 or mix4 == 13 or mix4 == 15 or mix4 == 18 or mix4 == 20 or mix4 == 22:
                if self.game.red_odds.position <= 1:
                    return 1
                else:
                    sd = self.game.spotting.position
                    mix3 = self.game.mixer3.position
                    if self.game.red_odds.position < 5:
                        i = self.check_red_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                    elif self.game.red_odds.position == 5:
                        if sd == 2 or sd == 4 or sd == 6 or sd == 7 or sd == 9 or sd == 10 or sd == 11 or sd == 12 or sd == 15 or sd == 16 or sd == 20 or sd == 21 or sd == 22 or sd == 29 or sd == 33 or sd == 34 or sd == 39 or sd == 40 or sd == 42 or sd == 44 or sd == 47:
                            i = self.check_red_mixer3()
                            if i == 1:
                                return 1
                            else:
                                return 0
                    elif self.game.red_odds.position == 6:
                        if sd == 8 or sd == 14 or sd == 15 or sd == 17 or sd == 19 or sd == 22 or sd == 23 or sd == 27 or sd == 29 or sd == 40 or sd == 41:
                            i = self.check_red_mixer3()
                            if i == 1:
                                return 1
                            else:
                                return 0
                    elif self.game.red_odds.position == 7:
                        if sd == 4 or sd == 10 or sd == 15 or sd == 39 or sd == 40 or sd == 48:
                            i = self.check_red_mixer3()
                            if i == 1:
                                return 1
                            else:
                                return 0
                    else:
                        return 0
            else:
                return 0
        else:
            if self.game.red_odds.position <= 1:
                return 1
            else:
                sd = self.game.spotting.position
                mix3 = self.game.mixer3.position
                if self.game.red_odds.position < 5:
                    i = self.check_red_mixer3()
                    if i == 1:
                        return 1
                    else:
                        return 0
                elif self.game.red_odds.position == 5:
                    if sd == 2 or sd == 4 or sd == 6 or sd == 7 or sd == 9 or sd == 10 or sd == 11 or sd == 12 or sd == 15 or sd == 16 or sd == 20 or sd == 21 or sd == 22 or sd == 29 or sd == 33 or sd == 34 or sd == 39 or sd == 40 or sd == 42 or sd == 44 or sd == 47:
                        i = self.check_red_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                elif self.game.red_odds.position == 6:
                    if sd == 8 or sd == 14 or sd == 15 or sd == 17 or sd == 19 or sd == 22 or sd == 23 or sd == 27 or sd == 29 or sd == 40 or sd == 41:
                        i = self.check_red_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                elif self.game.red_odds.position == 7:
                    if sd == 4 or sd == 10 or sd == 15 or sd == 39 or sd == 40 or sd == 48:
                        i = self.check_red_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                else:
                    return 0

    def check_red_mixer3(self):
        #CHECK MIXER3 after spotting disc position
        mix3 = self.game.mixer3.position
        if self.game.red_super_section.status == False:
            if mix3 == 5 or mix3 == 10:
                return 1
        if self.game.yellow_super_section.status == True:
            if mix3 == 14 or mix3 == 21:
                return 1
        if mix3 == 3 or mix3 == 9 or mix3 == 13 or mix3 == 17 or mix3 == 20 or mix3 == 23:
            return 1
        return 0

    def yellow_odds_probability(self):
        # Check position of Mixer 4, and Mixer 3 and current 
        # position of the odds, along with trip relays.
        # For first check, guaranteed double stepup.  Probability doesn't 
        # factor, so I will return as part of the initial check above.
        if self.game.before_fifth.status == True:
            mix4 = self.game.mixer4.position
            if mix4 == 3 or mix4 == 5 or mix4 == 7 or mix4 == 11 or mix4 == 13 or mix4 == 15 or mix4 == 18 or mix4 == 20 or mix4 == 22:
                if self.game.yellow_odds.position <= 1:
                    return 1
                else:
                    sd = self.game.spotting.position
                    mix3 = self.game.mixer3.position
                    if self.game.yellow_odds.position < 5:
                        i = self.check_yellow_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                    elif self.game.yellow_odds.position == 5:
                        if sd == 2 or sd == 4 or sd == 6 or sd == 7 or sd == 9 or sd == 10 or sd == 11 or sd == 12 or sd == 15 or sd == 16 or sd == 20 or sd == 21 or sd == 22 or sd == 29 or sd == 33 or sd == 34 or sd == 39 or sd == 40 or sd == 42 or sd == 44 or sd == 47:
                            i = self.check_yellow_mixer3()
                            if i == 1:
                                return 1
                            else:
                                return 0
                    elif self.game.yellow_odds.position == 6:
                        if sd == 8 or sd == 14 or sd == 15 or sd == 17 or sd == 19 or sd == 22 or sd == 23 or sd == 27 or sd == 29 or sd == 40 or sd == 41:
                            i = self.check_yellow_mixer3()
                            if i == 1:
                                return 1
                            else:
                                return 0
                    elif self.game.yellow_odds.position == 7:
                        if sd == 4 or sd == 10 or sd == 15 or sd == 39 or sd == 40 or sd == 48:
                            i = self.check_yellow_mixer3()
                            if i == 1:
                                return 1
                            else:
                                return 0
                    else:
                        return 0
            else:
                return 0
        else:
            if self.game.yellow_odds.position <= 1:
                return 1
            else:
                sd = self.game.spotting.position
                if self.game.yellow_odds.position < 5:
                    i = self.check_yellow_mixer3()
                    if i == 1:
                        return 1
                    else:
                        return 0
                elif self.game.yellow_odds.position == 5:
                    if sd == 2 or sd == 4 or sd == 6 or sd == 7 or sd == 9 or sd == 10 or sd == 11 or sd == 12 or sd == 15 or sd == 16 or sd == 20 or sd == 21 or sd == 22 or sd == 29 or sd == 33 or sd == 34 or sd == 39 or sd == 40 or sd == 42 or sd == 44 or sd == 47:
                        i = self.check_yellow_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                elif self.game.yellow_odds.position == 6:
                    if sd == 8 or sd == 14 or sd == 15 or sd == 17 or sd == 19 or sd == 22 or sd == 23 or sd == 27 or sd == 29 or sd == 40 or sd == 41:
                        i = self.check_yellow_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                elif self.game.yellow_odds.position == 7:
                    if sd == 4 or sd == 10 or sd == 15 or sd == 39 or sd == 40 or sd == 48:
                        i = self.check_yellow_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                else:
                    return 0

    def check_yellow_mixer3(self):
        #CHECK MIXER3 after spotting disc position
        mix3 = self.game.mixer3.position
        if self.game.red_super_section.status == True:
            if mix3 == 5 or mix3 == 10:
                return 1
        if self.game.yellow_super_section.status == False:
            if mix3 == 14 or mix3 == 21:
                return 1
        if mix3 == 2 or mix3 == 7 or mix3 == 8 or mix3 == 12 or mix3 == 16 or mix3 == 18:
            return 1
        return 0

    def green_odds_probability(self):
        # Check position of Mixer 4, and Mixer 3 and current 
        # position of the odds, along with trip relays.
        # For first check, guaranteed double stepup.  Probability doesn't 
        # factor, so I will return as part of the initial check above.
        if self.game.before_fifth.status == True:
            mix4 = self.game.mixer4.position
            if mix4 == 3 or mix4 == 5 or mix4 == 7 or mix4 == 11 or mix4 == 13 or mix4 == 15 or mix4 == 18 or mix4 == 20 or mix4 == 22:
                if self.game.green_odds.position <= 1:
                    return 1
                else:
                    sd = self.game.spotting.position
                    mix3 = self.game.mixer3.position
                    if self.game.green_odds.position < 5:
                        i = self.check_green_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                    elif self.game.green_odds.position == 5:
                        if sd == 2 or sd == 4 or sd == 6 or sd == 7 or sd == 9 or sd == 10 or sd == 11 or sd == 12 or sd == 15 or sd == 16 or sd == 20 or sd == 21 or sd == 22 or sd == 29 or sd == 33 or sd == 34 or sd == 39 or sd == 40 or sd == 42 or sd == 44 or sd == 47:
                            i = self.check_green_mixer3()
                            if i == 1:
                                return 1
                            else:
                                return 0
                    elif self.game.green_odds.position == 6:
                        if sd == 8 or sd == 14 or sd == 15 or sd == 17 or sd == 19 or sd == 22 or sd == 23 or sd == 27 or sd == 29 or sd == 40 or sd == 41:
                            i = self.check_green_mixer3()
                            if i == 1:
                                return 1
                            else:
                                return 0
                    elif self.game.green_odds.position == 7:
                        if sd == 4 or sd == 10 or sd == 15 or sd == 39 or sd == 40 or sd == 48:
                            i = self.check_green_mixer3()
                            if i == 1:
                                return 1
                            else:
                                return 0
                    else:
                        return 0
            else:
                return 0
        else:
            if self.game.green_odds.position <= 1:
                return 1
            else:
                sd = self.game.spotting.position
                if self.game.green_odds.position < 5:
                    i = self.check_green_mixer3()
                    if i == 1:
                        return 1
                    else:
                        return 0
                elif self.game.green_odds.position == 6:
                    if sd == 2 or sd == 4 or sd == 6 or sd == 7 or sd == 9 or sd == 10 or sd == 11 or sd == 12 or sd == 15 or sd == 16 or sd == 20 or sd == 21 or sd == 22 or sd == 29 or sd == 33 or sd == 34 or sd == 39 or sd == 40 or sd == 42 or sd == 44 or sd == 47:
                        i = self.check_green_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                elif self.game.green_odds.position == 7:
                    if sd == 8 or sd == 14 or sd == 15 or sd == 17 or sd == 19 or sd == 22 or sd == 23 or sd == 27 or sd == 29 or sd == 40 or sd == 41:
                        i = self.check_green_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                elif self.game.green_odds.position == 5:
                    if sd == 4 or sd == 10 or sd == 15 or sd == 39 or sd == 40 or sd == 48:
                        i = self.check_green_mixer3()
                        if i == 1:
                            return 1
                        else:
                            return 0
                else:
                    return 0

    def check_green_mixer3(self):
        #CHECK MIXER3 after spotting disc position
        mix3 = self.game.mixer3.position
        if mix3 == 1 or mix3 == 4 or mix3 == 6 or mix3 == 11 or mix3 == 15 or mix3 == 19 or mix3 == 22 or mix3 == 24:
            return 1
        else:
            return 0

    def check_mixer4(self):
        m4 = self.game.mixer4.position
        if self.game.green_odds.position >= 4:
            if m4 == 12 or m4 == 13 or m4 == 15 or m4 == 18 or m4 == 20 or m4 == 21:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.green_odds.position >= 5:
            if m4 == 4 or m4 == 6 or m4 == 12 or m4 == 15 or m4 == 18 or m4 == 20:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.green_odds.position >= 6:
            if m4 == 2 or m4 == 5 or m4 == 7 or m4 == 13 or m4 == 19:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.green_odds.position >= 7:
            if m4 == 10:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.green_odds.position >= 8:
            if m4 == 23:
                self.game.mixer4_relay.engage(self.game)
        if self.game.red_odds.position >= 4:
            if m4 == 7 or m4 == 8 or m4 == 12 or m4 == 13 or m4 == 17 or m4 == 18:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.red_odds.position >= 5:
            if m4 == 5 or m4 == 6 or m4 == 14 or m4 == 15 or m4 == 21:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.red_odds.position >= 6:
            if m4 == 3 or m4 == 4 or m4 == 10 or m4 == 16 or m4 == 20:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.red_odds.position >= 7:
            if m4 == 11 or m4 == 19 or m4 == 22:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.red_odds.position >= 8:
            if m4 == 23:
                self.game.mixer4_relay.engage(self.game)
        if self.game.yellow_odds.position >= 4:
            if m4 == 9 or m4 == 10 or m4 == 12 or m4 == 13 or m4 == 15 or m4 == 16:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.yellow_odds.position >= 5:
            if m4 == 4 or m4 == 5 or m4 == 6 or m4 == 8 or m4 == 14 or m4 == 18 or m4 == 19:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.yellow_odds.position >= 6:
            if m4 == 11 or m4 == 17 or m4 == 21:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.yellow_odds.position >= 7:
            if m4 == 7 or m4 == 20 or m4 == 22:
                self.game.mixer4_relay.engage(self.game)
        elif self.game.yellow_odds.position >= 8:
            if m4 == 23:
                self.game.mixer4_relay.engage(self.game)


    def scan_features(self):
        p = self.features_probability()

    def features_probability(self):
        s = random.randint(1,4)
        self.animate_feature_scan(s)
        self.check_mixer4()
        if self.game.mixer4_relay.status == False:
            self.features_spotting()
        else:
            self.game.mixer4_relay.disengage()

    def features_spotting(self):
        sd = self.game.spotting.position
        # Check Magic Screen and trip relays.
        # First, Magic Screen Feature Unit steps
        # Guaranteed step first, otherwise, the game will auto-step twice on first award.
        if self.game.magic_screen_feature.position == 1 or self.game.magic_screen_feature.position == 2:
            self.game.magic_screen_feature.step()
            if self.game.magic_screen_feature.position == 7:
                if self.game.before_fifth.status == False:
                    self.game.before_fourth.engage(self.game)
        if self.game.reflex.position > 0:
            if sd == 8 or sd == 15 or sd == 23 or sd == 29:
                if self.game.magic_screen_feature.position == 0:
                    self.game.magic_screen_feature.step()
                    if self.game.magic_screen_feature.position == 7:
                        if self.game.before_fifth.status == False:
                            self.game.before_fourth.engage(self.game)
        if sd == 0 or sd == 25:
            if self.game.magic_screen_feature.position == 0:
                self.game.magic_screen_feature.step()
                if self.game.magic_screen_feature.position == 7:
                    if self.game.before_fifth.status == False:
                        self.game.before_fourth.engage(self.game)
        if sd == 2 or sd == 5 or sd == 6 or sd == 10 or sd == 12 or sd == 16 or sd == 20 or sd == 26 or sd == 30 or sd == 38 or sd == 42 or sd == 43 or sd == 44 or sd == 48:
            print "HERE"
            if self.game.magic_screen_feature.position < 7:
                if self.game.red_super_section.status == False and self.game.yellow_super_section.status == False:
                    self.step_magic_screen(7 - self.game.magic_screen_feature.position)
            else:
                if self.game.magic_screen_feature.position >= 7 and self.game.magic_screen_feature.position < 9:
                    self.game.magic_screen_feature.step()
                    if self.game.magic_screen_feature.position == 7:
                        if self.game.before_fifth.status == False:
                            self.game.before_fourth.engage(self.game)
        if sd == 3 or sd == 7 or sd == 11 or sd == 13:
            self.step_magic_screen(10)
        
        # Super sections only enabled (one or the other), if MS is up to D or more.
        if self.game.magic_screen_feature.position >= 7:
            if sd == 8 or sd == 26 or sd == 43 or sd == 46:
                if self.game.cu == 1:
                    if self.game.yellow_super_section.status == False:
                        self.game.red_super_section.engage(self.game)
                else:
                    if self.game.red_super_section.status == False:
                        self.game.yellow_super_section.engage(self.game)

        # Blue 'super section' - 2 in the blue.
        if sd == 4 or sd == 9 or sd == 45 or sd == 49 or sd == 31:
            self.game.three_blue.disengage()
            self.game.two_blue.engage(self.game)

        # Rollover enabling - both enable at once on this game
        if sd == 24 or sd == 32 or sd == 36 or sd == 37 or sd == 46:
            if self.game.red_star.status == False:
                self.game.red_star.engage(self.game)
                self.game.coils.yellowROLamp.enable()
            if self.game.yellow_star.status == False:
                self.game.yellow_star.engage(self.game)
                self.game.coils.redROLamp.enable()

        # Before Fifth
        if sd == 39:
            self.game.before_fifth.engage(self.game)

    def step_magic_screen(self, number):
        if number >= 1:
            self.game.magic_screen_feature.step()
            if self.game.magic_screen_feature.position == 7:
                if self.game.before_fifth.status == False:
                    self.game.before_fourth.engage(self.game)
            number -= 1
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
            self.delay(name="step_sc", delay=0.1, handler=self.step_magic_screen, param=number)

    def scan_eb(self):
        s = random.randint(1,3)
        self.animate_eb_scan(s)
        if self.game.extra_ball.position == 0:
            self.game.extra_ball.step()
            self.check_lifter_status()
        p = self.eb_probability()
                                
        # Timer resets to 0 position on ball count increasing.  We are fudging this since we will have
        # no good way to measure balls as they return back to the trough.  The ball count unit cannot be
        # relied upon as we do not have a switch in the outhole, and the trough logic is too complex for
        # the task at hand.
        # TODO: implement thunk noises into the units.py to automatically play the noises.
        self.game.timer.reset()
        self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def animate_odds_scan(self, s):
        if s > 1:
            self.delay(name="odds_animation", delay=0.1, handler=graphics.carnival_queen.odds_animation, param=s)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
            s -= 1
            #self.delay(name="animate_odds", delay=0.1, handler=self.animate_odds_scan, param=s)
        else:
            self.cancel_delayed(name="odds_animation")
            self.cancel_delayed(name="display")

    def animate_feature_scan(self, s):
        if s > 1:
            self.delay(name="feature_animation", delay=0.1, handler=graphics.carnival_queen.feature_animation, param=s)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
            s -= 1
            #self.delay(name="animate_feature", delay=0.1, handler=self.animate_feature_scan, param=s)
        else:
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def animate_eb_scan(self, s):
        if s > 1:
            self.delay(name="eb_animation", delay=0.1, handler=graphics.carnival_queen.eb_animation, param=s)
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
            s -= 1
            #self.delay(name="animate_eb", delay=0.1, handler=self.animate_eb_scan, param=s)
        else:
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)

    def eb_probability(self):
        mix2 = self.game.mixer2.position
        if self.game.cu == 0:
            if self.game.magic_screen_feature.position <= 6:
                i = self.check_eb_steps()
            elif self.game.magic_screen_feature.position == 7:
                if mix2 % 4 == 0:
                    i = self.check_eb_steps()
            elif self.game.magic_screen_feature.position == 8:
                if mix2 % 3 == 0:
                    i = self.check_eb_steps()
            elif self.game.magic_screen_feature.position == 9:
                if mix2 % 2 == 0:
                    i = self.check_eb_steps()
            else:
                if mix2 % 5 == 0:
                    i = self.check_eb_steps()
        else:
            i = self.check_eb_steps()

        return i

    def check_eb_steps(self):
        sd = self.game.spotting.position
        mix3 = self.game.mixer3.position
        if sd == 0:
            if mix3 % 2 == 0:
                self.step_eb(9)
        if sd == 1 or sd == 2 or sd == 6 or sd == 7 or sd == 15 or sd == 17 or sd == 23 or sd == 29 or sd == 33 or sd == 34 or sd == 35 or sd == 38 or sd == 39 or sd == 40 or sd == 42 or sd == 44 or sd == 45 or sd == 47 or sd == 48 or sd == 49:
            if mix3 % 2 == 1:
                if self.game.extra_ball.position < 3:
                    self.step_eb(3 - self.game.extra_ball.position)
                elif self.game.extra_ball.position >= 3 and self.game.extra_ball.position < 6:
                    self.step_eb(6 - self.game.extra_ball.position)
                elif self.game.extra_ball.position >= 6:
                    self.step_eb(9 - self.game.extra_ball.position)
            else:
                self.step_eb(1)

    def step_eb(self, number):
        if number >= 1:
            self.game.extra_ball.step()
            self.check_lifter_status()
            number -= 1
            self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
            self.delay(name="step_eb", delay=0.1, handler=self.step_eb, param=number)

    def blink_title(self):
        title1 = random.randint(0,1)
        title2 = random.randint(0,1)
        title3 = random.randint(0,1)
        title4 = random.randint(0,1)
        if title1 == 1:
            pos = [167,257]
            image = pygame.image.load('carnival_queen/assets/title1_on.png').convert_alpha()
            screen.blit(image, pos)
        if title2 == 1:
            pos = [241,290]
            image = pygame.image.load('carnival_queen/assets/title2_on.png').convert_alpha()
            screen.blit(image, pos)
        if title3 == 1:
            pos = [346,298]
            image = pygame.image.load('carnival_queen/assets/title3_on.png').convert_alpha()
            screen.blit(image, pos)
        if title4 == 1:
            pos = [431,264]
            image = pygame.image.load('carnival_queen/assets/title4_on.png').convert_alpha()
            screen.blit(image, pos)
            
        pygame.display.update()
        self.delay(name="display", delay=0.1, handler=graphics.carnival_queen.display, param=self)
#        self.delay(name="blink_title", delay=3, handler=self.blink_title)

    # Define reset as the knock-off, anti-cheat relay disabled, and replay reset enabled.  Motors turn while credits are knocked off.
    # When meter reaches zero and the zero limit switch is hit, turn off motor sound and leave backglass gi on, but with tilt displayed.

    def startup(self):        
        # Every bingo requires the meter to register '0' 
        # before allowing coin entry --
        # also needs to show a plain 'off' backglass.
        self.eb = False
        self.game.anti_cheat.engage(self.game)
        self.tilt_actions()
#        self.delay(name="blink_title", delay=1, handler=self.blink_title)


class CarnivalQueen(procgame.game.BasicGame):
    """ Palm Beach was the first game with Super Cards """
    def __init__(self, machine_type):
        super(CarnivalQueen, self).__init__(machine_type)
        pygame.mixer.pre_init(44100,-16,2,512)
        self.sound = procgame.sound.SoundController(self)
        self.sound.set_volume(1.0)
        # NOTE: trough_count only counts the number of switches present in the  trough.  It does _not_ count
        #       the number of balls present.   In this game, there  should  be  8  balls.
        self.trough_count = 6

        # Now, the control unit can be in one of two positions, essentially.
        # This alternates by coin, and is used to portion the Spotted Numbers.
        self.cu = 1

        # Subclass my units unique to this game -  modifications must be made to set up mixers and steppers unique to the game
        # NOTE: 'top' positions are indexed using a 0 index, so the top on a 24 position unit is actually 23.

        self.mixer1 = units.Mixer("mixer1", 23)
        self.mixer2 = units.Mixer("mixer2", 23)
        self.mixer3 = units.Mixer("mixer3", 23)
        self.mixer4 = units.Mixer("mixer4", 23)

        self.searchdisc = units.Search("searchdisc", 12)

        #Search relays
        self.s1 = units.Relay("s1")
        self.s2 = units.Relay("s2")
        self.s3 = units.Relay("s3")
        self.s4 = units.Relay("s4")
        self.s5 = units.Relay("s5")
        self.search_index = units.Relay("search_index")

        #Odds steppers
        self.red_odds = units.Stepper("red_odds", 8, 'carnival_queen')
        self.yellow_odds = units.Stepper("yellow_odds", 8, 'carnival_queen')
        self.green_odds = units.Stepper("green_odds", 8, 'carnival_queen')

        #Replay Counter
        self.red_replay_counter = units.Stepper("red_replay_counter", 600)
        self.yellow_replay_counter = units.Stepper("yellow_replay_counter", 600)
        self.green_replay_counter = units.Stepper("green_replay_counter", 600)

        self.yellow_super_section = units.Relay("yellow_super_section")
        self.red_super_section = units.Relay("red_super_section")
        self.before_fourth = units.Relay("before_fourth")
        self.before_fifth = units.Relay("before_fifth")
        self.three_blue = units.Relay("three_blue")
        self.two_blue = units.Relay("two_blue")

        #Initialize stepper units used to keep track of features or timing.
        self.timer = units.Stepper("timer", 40)
        self.ball_count = units.Stepper("ball_count", 8)

        # Initialize reflex(es) and mixers unique to this game
        # NOTE: reflex unit drawing was not available for this game, so until I convince
        #       another Palm Beach owner to take their game apart, I'll note that there
        #       are five lugs, four of which provide another path to the mixer, and one which is always connected
        #       and bypasses the mixer entirely.  There are no games from 1951 or 52 that have the reflex documented.
        self.reflex = units.Reflex("primary", 200)

        #This is a disc which has 50 positions
        #and will randomly complete paths through the various mixers to allow for odds or feature step.
        self.spotting = units.Spotting("spotting", 50)

        #Check for status of the replay register zero switch.  If positive
        #and machine is just powered on, this will zero out the replays.
        self.replay_reset = units.Relay("replay_reset")
        
        #Extra ball unit contains 24 positions.
        self.extra_ball = units.Stepper("extra_ball", 21)

        #When engage()d, light 6v circuit, and enable game features, scoring,
        #etc. Disengage()d means that the machine is 'soft' tilted. 
        self.anti_cheat = units.Relay("anti_cheat")

        #When engage()d, spin.
        self.start = units.Relay("start")

        #Tilt is separate from anti-cheat in that the trip will move the shutter
        #when the game is tilted with 1st ball in the lane.  Also prevents you
        #from picking back up by killing the anti-cheat.  Can be engaged by 
        #tilt bob, slam tilt switches, or timer at 39th step.
        #Immediately kills motors.
        self.tilt = units.Relay("tilt")

        #Need to define relays for playing for ebs
        self.eb_play = units.Relay("eb_play")

        self.selector = units.Stepper("selector", 1)

        self.magic_screen_feature = units.Stepper("magic_screen_feature", 10)

        self.magic_screen = units.Stepper("magic_screen", 7)

        #Some special trip relays for spotted numbers and rollovers
        self.red_star = units.Relay("red_star")
        self.yellow_star = units.Relay("yellow_star")

        self.replays = 0
        self.returned = False

        self.mixer4_relay = units.Relay("mixer4_relay")

    def reset(self):
        super(CarnivalQueen, self).reset()
        self.logger = logging.getLogger('game')
        self.load_config('bingo.yaml')
        
        main_mode = SinglecardBingo(self)
        self.modes.add(main_mode)
        
game = CarnivalQueen(machine_type='pdb')
game.reset()
game.run_loop()
