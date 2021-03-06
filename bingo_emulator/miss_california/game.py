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
from bingo_emulator.graphics.miss_california import *

class MulticardBingo(procgame.game.Mode):
    def __init__(self, game):
        super(MulticardBingo, self).__init__(game=game, priority=5)
        self.holes = []
        self.startup()
        self.game.sound.register_music('motor', "audio/woodrail_motor.wav")
        self.game.sound.register_music('search1', "audio/automatic_search_one_ball.wav")
        self.game.sound.register_music('search2', "audio/automatic_search_two_ball.wav")
        self.game.sound.register_music('search3', "audio/automatic_search_three_ball.wav")
        self.game.sound.register_music('search4', "audio/automatic_search_four_ball.wav")
        self.game.sound.register_music('search5', "audio/automatic_search_five_ball.wav")
        self.game.sound.register_music('search6', "audio/automatic_search_six_ball.wav")
        self.game.sound.register_music('search7', "audio/automatic_search_seven_ball.wav")
        self.game.sound.register_music('search8', "audio/automatic_search_eight_ball.wav")
        self.game.sound.register_sound('add', "audio/woodrail_coin.wav")
        self.game.sound.register_sound('tilt', "audio/tilt.wav")
        self.game.sound.register_sound('step', "audio/step.wav")
        self.game.sound.register_sound('eb_search', "audio/EB_Search.wav")

    def sw_coin_active(self, sw):
        self.game.sound.stop('add')
        self.game.sound.play('add')
        self.regular_play()
        self.game.tilt.disengage()
        self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_startButton_active(self, sw):
        self.cancel_delayed(name="both_animation")
        if self.game.replays > 0 or self.game.switches.freeplay.is_active():
            self.game.sound.stop('add')
            self.game.sound.play('add')
            self.game.tilt.disengage()
            self.regular_play()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_trough4_active_for_1s(self, sw):
        if self.game.ball_count.position >= 4:
            self.timeout_actions()
    
    def timeout_actions(self):
        if (self.game.timer.position < 39):
            self.game.timer.step()
            self.delay(name="timeout", delay=5.0, handler=self.timeout_actions)
        else:
            self.game.timer.step()
            self.tilt_actions()


    def sw_trough8_closed(self, sw):
        if self.game.start.status == False:
            self.game.ball_count.position -= 1
            self.game.returned = True
            self.check_lifter_status()
        else:
            self.check_lifter_status()

    def sw_enter_active(self, sw):
        if self.game.switches.left.is_active() and self.game.switches.right.is_active():
            self.game.end_run_loop()
            os.system("/home/nbaldridge/proc/bingo_emulator/start_game.sh miss_california")
            

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
        self.cancel_delayed(name="both_animation")
        self.cancel_delayed(name="search")
        self.cancel_delayed(name="card1_replay_step_up")
        self.cancel_delayed(name="card2_replay_step_up")
        self.cancel_delayed(name="card3_replay_step_up")
        self.cancel_delayed(name="corners_replay_step_up")
        self.cancel_delayed(name="timeout")
        self.game.search_index.disengage()
        self.game.coils.counter.pulse()

        self.game.cu = not self.game.cu
        begin = self.game.spotting.position
        self.game.spotting.spin()
        self.game.mixer1.spin()
        self.game.mixer2.spin()
        self.game.mixer3.spin()
        self.game.reflex.decrease()
        self.animate_both([begin,self.game.spotting.movement_amount,1])
 
        self.game.returned = False
        if self.game.start.status == True:
            if self.game.selector.position < 3:
                self.game.selector.step()
            if self.game.switches.shutter.is_inactive():
                self.game.coils.shutter.enable()
            self.replay_step_down()
            graphics.miss_california.display(self)
            self.check_lifter_status()
        else:
            self.holes = []
            self.game.start.engage(self.game)
            self.game.corners_replay_counter.reset()
            self.game.c1_double.disengage()
            self.game.c2_double.disengage()
            self.game.c3_double.disengage()
            self.game.timer.reset()
            self.game.card1_replay_counter.reset()
            self.game.card2_replay_counter.reset()
            self.game.card3_replay_counter.reset()
            self.game.corners.disengage()
            self.game.start.engage(self.game)
            self.game.selector.reset()
            self.game.ball_count.reset()
            self.game.sound.play_music('motor', -1)
            self.regular_play()
        self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)
        self.game.tilt.disengage()

    def check_lifter_status(self):
        if self.game.tilt.status == False:
            if self.game.switches.trough8.is_closed() and self.game.switches.trough5.is_open() and self.game.switches.trough4.is_open() and self.game.switches.trough3.is_closed() and self.game.switches.trough2.is_closed():
                if self.game.switches.shooter.is_open():
                    self.game.coils.lifter.enable()
                    self.game.returned = False
            else:
                if self.game.start.status == False:
                    if self.game.switches.trough4.is_open():
                        if self.game.switches.shooter.is_open():
                            if self.game.switches.gate.is_closed():
                                self.game.coils.lifter.enable()
                    else:
                        if self.game.returned == True and self.game.ball_count.position == 4:
                            if self.game.switches.shooter.is_open():
                                self.game.coils.lifter.enable()
                                self.game.returned = False

    def sw_smRunout_active_for_1ms(self, sw):
        if self.game.start.status == True:
            self.check_shutter(1)
        else:
            self.check_shutter()

    def sw_trough1_closed(self, sw):
        if self.game.switches.shooter.is_closed():
            self.game.coils.lifter.disable()

    def sw_shooter_active(self, sw):
        if (self.game.ball_count.position >= 7 and self.game.switches.trough1.is_inactive()):
            self.game.coils.lifter.disable()

    def sw_ballLift_active_for_500ms(self, sw):
        if self.game.tilt.status == False:
            if self.game.switches.shooter.is_open():
                if self.game.ball_count.position < 5:
                    self.game.coils.lifter.enable()

    def sw_gate_inactive_for_1ms(self, sw):
        self.game.start.disengage()
        self.game.ball_count.step()
        if self.game.switches.shutter.is_active():
            self.game.coils.shutter.enable()
        if self.game.ball_count.position == 4:
            self.game.sound.play('tilt')
            self.game.sound.play('tilt')
        if self.game.ball_count.position >= 4:
            if self.game.search_index.status == False:
                self.search()
        if self.game.ball_count.position <= 4:
            self.check_lifter_status()

    # This is really nasty, but it is how we render graphics for each individual hole.
    # numbers are added (or removed from) a list.  In this way, I can re-use the same
    # routine even for games where there are ball return functions like Surf Club.

    def sw_hole1_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(1)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole2_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(2)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole3_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(3)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole4_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(4)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole5_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(5)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole6_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(6)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole7_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(7)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole8_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(8)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole9_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(9)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole10_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(10)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole11_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(11)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole12_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(12)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole13_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(13)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole14_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(14)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole15_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(15)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole16_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(16)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole17_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(17)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole18_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(18)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole19_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(19)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole20_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(20)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole21_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(21)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole22_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(22)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole23_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(23)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole24_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(24)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def sw_hole25_active_for_40ms(self, sw):
        if self.game.tilt.status == False and self.game.start.status == False:
            self.holes.append(25)
            if self.game.ball_count.position >= 4:
                if self.game.search_index.status == False:
                    self.search()
            self.search_sounds()
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)
    
    def sw_replayReset_active(self, sw):
        self.game.anti_cheat.disengage()
        self.holes = []
        graphics.miss_california.display(self)
        self.tilt_actions()
        self.replay_step_down(self.game.replays)

    def tilt_actions(self):
        self.game.start.disengage()
        self.cancel_delayed(name="replay_reset")
        self.cancel_delayed(name="card1_replay_step_up")
        self.cancel_delayed(name="card2_replay_step_up")
        self.cancel_delayed(name="card3_replay_step_up")
        self.cancel_delayed(name="corners_replay_step_up")
        self.cancel_delayed(name="timeout")
        self.game.search_index.disengage()
        if self.game.ball_count.position == 0:
            if self.game.switches.shutter.is_active():
                self.game.coils.shutter.enable()
        self.holes = []
        self.game.selector.reset()
        self.game.corners.disengage()
        self.game.c1_double.disengage()
        self.game.c2_double.disengage()
        self.game.c3_double.disengage()
        self.game.corners.disengage()
        self.game.ball_count.reset()
        self.game.anti_cheat.engage(game)
        self.game.tilt.engage(self.game)
        self.game.sound.stop_music()
        self.game.sound.play('tilt')
        # displays "Tilt" on the backglass, you have to recoin.
        self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)

    def search_sounds(self):
        self.game.sound.stop_music()
        if self.game.ball_count.position == 1:
            self.game.sound.play_music('search1', -1)
        if self.game.ball_count.position == 2:
            self.game.sound.play_music('search2', -1)
        if self.game.ball_count.position == 3:
            self.game.sound.play_music('search3', -1)
        if self.game.ball_count.position == 4:
            self.game.sound.play_music('search4', -1)
        if self.game.ball_count.position == 5:
            self.game.sound.play_music('search5', -1)
        if self.game.ball_count.position == 6:
            self.game.sound.play_music('search6', -1)
        if self.game.ball_count.position == 7:
            self.game.sound.play_music('search7', -1)
        if self.game.ball_count.position == 8:
            self.game.sound.play_music('search8', -1)

    def sw_tilt_active(self, sw):
        if self.game.tilt.status == False:
            self.tilt_actions()

    def replay_step_down(self, number=0):
        if number > 0:
            if number > 1:
                self.game.replays -= 1
                graphics.replay_step_down(self.game.replays, graphics.miss_california.reel1, graphics.miss_california.reel10, graphics.miss_california.reel100)
                self.game.coils.registerDown.pulse()
                number -= 1
                graphics.miss_california.display(self)
                self.delay(name="replay_reset", delay=0.13, handler=self.replay_step_down, param=number)
            elif number == 1:
                self.game.replays -= 1
                graphics.replay_step_down(self.game.replays, graphics.miss_california.reel1, graphics.miss_california.reel10, graphics.miss_california.reel100)
                self.game.coils.registerDown.pulse()
                number -= 1
                graphics.miss_california.display(self)
                self.cancel_delayed(name="replay_reset")
        else: 
            if self.game.replays > 0:
                self.game.replays -= 1
                graphics.replay_step_down(self.game.replays, graphics.miss_california.reel1, graphics.miss_california.reel10, graphics.miss_california.reel100)
                self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)
            self.game.coils.registerDown.pulse()

    def replay_step_up(self):
        if self.game.replays < 899:
            self.game.replays += 1
            graphics.replay_step_up(self.game.replays, graphics.miss_california.reel1, graphics.miss_california.reel10, graphics.miss_california.reel100)
        self.game.coils.registerUp.pulse()
        self.game.coils.sounder.pulse()
        self.game.reflex.increase()
        graphics.miss_california.display(self)

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

        for i in range(0, 50):
            self.r = self.closed_search_relays(self.game.searchdisc.position, self.game.corners.status)
            self.game.searchdisc.spin()
            self.wipers = self.r[0]
            self.card = self.r[1]
            self.corners = self.r[2]

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
                        for i in relays:
                            pass
                        s = functions.count_seq(relays)
                        if self.game.selector.position >= self.card:
                            if s >= 3:
                                self.find_winner(s, self.game.selector.position, self.card, self.corners)
                                break

    def find_winner(self, relays, selector, card, corners):
        if self.game.search_index.status == False and self.game.replays < 899:
            if selector >= 1:
                if card == 1:
                    if relays == 3:
                        if corners:
                            pass
                        elif self.game.c1_double.status == True:
                            if self.game.card1_replay_counter.position < 8:
                                self.game.search_index.engage(self.game)
                                self.card1_replay_step_up(8 - self.game.card1_replay_counter.position)
                        elif self.game.card1_replay_counter.position < 4:
                            self.game.search_index.engage(self.game)
                            self.card1_replay_step_up(4 - self.game.card1_replay_counter.position)
                    if relays == 4:
                        if corners and self.game.corners.status == True:
                            if self.game.corners_replay_counter.position < 200:
                                self.game.search_index.engage(self.game)
                                self.corners_replay_step_up(200 - self.game.corners_replay_counter.position)
                        else:
                            if self.game.c1_double.status == True:
                                if self.game.card1_replay_counter.position < 40:
                                    self.game.search_index.engage(self.game)
                                    self.card1_replay_step_up(40 - self.game.card1_replay_counter.position)
                            elif self.game.card1_replay_counter.position < 20:
                                self.game.search_index.engage(self.game)
                                self.card1_replay_step_up(20 - self.game.card1_replay_counter.position)
                    if relays == 5:
                        if self.game.c1_double.status == True:
                            if self.game.card1_replay_counter.position < 200:
                                self.game.search_index.engage(self.game)
                                self.card1_replay_step_up(200 - self.game.card1_replay_counter.position)
                        elif self.game.card1_replay_counter.position < 100:
                            self.game.search_index.engage(self.game)
                            self.card1_replay_step_up(100 - self.game.card1_replay_counter.position)
            if selector >= 2:
                if card == 2:
                    if relays == 3:
                        if corners:
                            pass
                        if self.game.c2_double.status == True:
                            if self.game.card2_replay_counter.position < 8:
                                self.game.search_index.engage(self.game)
                                self.card2_replay_step_up(8 - self.game.card2_replay_counter.position)
                        elif self.game.card2_replay_counter.position < 4:
                            self.game.search_index.engage(self.game)
                            self.card2_replay_step_up(4 - self.game.card2_replay_counter.position)
                    if relays == 4:
                        if corners and self.game.corners.status == True:
                            if self.game.corners_replay_counter.position < 200:
                                self.game.search_index.engage(self.game)
                                self.corners_replay_step_up(200 - self.game.corners_replay_counter.position)
                        else:
                            if self.game.c1_double.status == True:
                                if self.game.card2_replay_counter.position < 40:
                                    self.game.search_index.engage(self.game)
                                    self.card2_replay_step_up(40 - self.game.card2_replay_counter.position)
                            elif self.game.card2_replay_counter.position < 20:
                                self.game.search_index.engage(self.game)
                                self.card2_replay_step_up(20 - self.game.card2_replay_counter.position)
                    if relays == 5:
                        if self.game.c1_double.status == True:
                            if self.game.card2_replay_counter.position < 200:
                                self.game.search_index.engage(self.game)
                                self.card2_replay_step_up(200 - self.game.card2_replay_counter.position)
                        elif self.game.card2_replay_counter.position < 100:
                            self.game.search_index.engage(self.game)
                            self.card2_replay_step_up(100 - self.game.card2_replay_counter.position)
            if selector >= 3:
                if card == 3:
                    if relays == 3:
                        if corners:
                            pass
                        if self.game.c3_double.status == True:
                            if self.game.card3_replay_counter.position < 8:
                                self.game.search_index.engage(self.game)
                                self.card3_replay_step_up(8 - self.game.card3_replay_counter.position)
                        elif self.game.card3_replay_counter.position < 4:
                            self.game.search_index.engage(self.game)
                            self.card3_replay_step_up(4 - self.game.card3_replay_counter.position)
                    if relays == 4:
                        if corners and self.game.corners.status == True:
                            if self.game.corners_replay_counter.position < 200:
                                self.game.search_index.engage(self.game)
                                self.corners_replay_step_up(200 - self.game.corners_replay_counter.position)
                        else:
                            if self.game.c1_double.status == True:
                                if self.game.card3_replay_counter.position < 40:
                                    self.game.search_index.engage(self.game)
                                    self.card3_replay_step_up(40 - self.game.card3_replay_counter.position)
                            elif self.game.card3_replay_counter.position < 20:
                                self.game.search_index.engage(self.game)
                                self.card3_replay_step_up(20 - self.game.card3_replay_counter.position)
                    if relays == 5:
                        if self.game.c1_double.status == True:
                            if self.game.card3_replay_counter.position < 200:
                                self.game.search_index.engage(self.game)
                                self.card3_replay_step_up(200 - self.game.card3_replay_counter.position)
                        elif self.game.card3_replay_counter.position < 100:
                            self.game.search_index.engage(self.game)
                            self.card3_replay_step_up(100 - self.game.card3_replay_counter.position)

    def card1_replay_step_up(self, number):
        self.game.sound.stop_music()
        if number >= 1:
            self.game.card1_replay_counter.step()
            number -= 1
            self.replay_step_up()
            if self.game.replays == 899:
                number = 0
            self.delay(name="card1_replay_step_up", delay=0.25, handler=self.card1_replay_step_up, param=number)
        else:
            self.game.search_index.disengage()
            self.cancel_delayed(name="card1_replay_step_up")
            self.search_sounds()
            self.search()

    def card2_replay_step_up(self, number):
        self.game.sound.stop_music()
        if number >= 1:
            self.game.card2_replay_counter.step()
            number -= 1
            self.replay_step_up()
            if self.game.replays == 899:
                number = 0
            self.delay(name="card2_replay_step_up", delay=0.25, handler=self.card2_replay_step_up, param=number)
        else:
            self.game.search_index.disengage()
            self.cancel_delayed(name="card2_replay_step_up")
            self.search_sounds()
            self.search()

    def card3_replay_step_up(self, number):
        self.game.sound.stop_music()
        if number >= 1:
            self.game.card3_replay_counter.step()
            number -= 1
            self.replay_step_up()
            if self.game.replays == 899:
                number = 0
            self.delay(name="card3_replay_step_up", delay=0.25, handler=self.card3_replay_step_up, param=number)
        else:
            self.game.search_index.disengage()
            self.cancel_delayed(name="card3_replay_step_up")
            self.search_sounds()
            self.search()

    def corners_replay_step_up(self, number):
        self.game.sound.stop_music()
        if number >= 1:
            self.game.corners_replay_counter.step()
            number -= 1
            self.replay_step_up()
            if self.game.replays == 899:
                number = 0
            self.delay(name="corners_replay_step_up", delay=0.25, handler=self.corners_replay_step_up, param=number)
        else:
            self.game.search_index.disengage()
            self.cancel_delayed(name="corners_replay_step_up")
            self.search_sounds()
            self.search()

    def closed_search_relays(self, rivets, c):
        # This function is critical, as it will determine which card is returned, etc.  I need to check the position of the
        # replay counter for the card. We will get a row back
        # that has the numbers on the position which will return the search relay connected.  When three out of the five relays
        # are connected, we get a winner!
        
        self.pos = {}
        # Card 1
        # Search disc also not documented.
        self.pos[0] = {}
        self.pos[1] = {5:1, 1:2, 9:3, 25:4, 3:5}
        self.pos[2] = {8:1, 22:2, 10:3, 19:4, 17:5}
        self.pos[3] = {6:1, 18:2, 16:3, 11:4, 7:5}
        self.pos[4] = {24:1, 21:2, 14:3, 20:4, 13:5}
        self.pos[5] = {12:1, 23:2, 2:3, 15:4, 4:5}
        self.pos[6] = {5:1, 8:2, 6:3, 24:4, 12:5}
        self.pos[7] = {1:1, 22:2, 18:3, 21:4, 23:5}
        self.pos[8] = {9:1, 10:2, 16:3, 14:4, 2:5}
        self.pos[9] = {25:1, 19:2, 11:3, 20:4, 15:5}
        self.pos[10] = {3:1, 17:2, 7:3, 13:4, 4:5}
        self.pos[11] = {5:1, 22:2, 16:3, 20:4, 4:5}
        self.pos[12] = {3:1, 19:2, 16:3, 21:4, 12:5}
        self.pos[13] = {5:1, 3:2, 12:3, 4:4}
        self.pos[14] = {}
        self.pos[15] = {9:1, 24:2, 4:3, 16:4, 6:5}
        self.pos[16] = {13:1, 19:2, 14:3, 20:4, 25:5}
        self.pos[17] = {2:1, 18:2, 15:3, 12:4, 8:5}
        self.pos[18] = {1:1, 22:2, 11:3, 21:4, 17:5}
        self.pos[19] = {10:1, 7:2, 5:3, 23:4, 3:5}
        self.pos[20] = {9:1, 13:2, 2:3, 1:4, 10:5}
        self.pos[21] = {24:1, 19:2, 18:3, 22:4, 7:5}
        self.pos[22] = {4:1, 14:2, 15:3, 11:4, 5:5}
        self.pos[23] = {16:1, 20:2, 12:3, 21:4, 23:5}
        self.pos[24] = {6:1, 25:2, 8:3, 17:4, 3:5}
        self.pos[25] = {9:1, 19:2, 15:3, 21:4, 3:5}
        self.pos[26] = {6:1, 20:2, 15:3, 22:4, 10:5}
        self.pos[27] = {9:1, 6:2, 10:3, 3:4}
        self.pos[28] = {}
        self.pos[29] = {21:1, 7:2, 10:3, 4:4, 9:5}
        self.pos[30] = {15:1, 3:2, 18:3, 22:4, 8:5}
        self.pos[31] = {24:1, 14:2, 17:3, 11:4, 2:5}
        self.pos[32] = {13:1, 6:2, 12:3, 19:4, 23:5}
        self.pos[33] = {20:1, 25:2, 1:3, 16:4, 5:5}
        self.pos[34] = {21:1, 15:2, 24:3, 13:4, 20:5}
        self.pos[35] = {7:1, 3:2, 14:3, 6:4, 25:5}
        self.pos[36] = {10:1, 18:2, 17:3, 12:4, 1:5}
        self.pos[37] = {4:1, 22:2, 11:3, 19:4, 16:5}
        self.pos[38] = {9:1, 8:2, 2:3, 23:4, 5:5}
        self.pos[39] = {21:1, 3:2, 17:3, 19:4, 5:5}
        self.pos[40] = {9:1, 22:2, 17:3, 6:4, 20:5}
        self.pos[41] = {21:1, 9:2, 20:3, 5:4}
        self.pos[42] = {}
        self.pos[43] = {}
        self.pos[44] = {}
        self.pos[45] = {}
        self.pos[46] = {}
        self.pos[47] = {}
        self.pos[48] = {}
        self.pos[49] = {}
        self.pos[50] = {}

        corners = False
        card = 0

        if c:
            if rivets == 13 or rivets == 27 or rivets == 41:
                corners = True
        if rivets in range(0,14):
            card = 1
        elif rivets in range(15,28):
            card = 2
        elif rivets in range(29, 42):
            card = 3

        return (self.pos[rivets], card, corners)
    
    def scan_all(self):
        #Animate scanning of everything - this happens through the spotting disc
        self.all_probability()

    def all_probability(self):
       
        mix1 = self.game.mixer1.connected_rivet()
        if self.game.reflex.connected_rivet() == 1:
            self.scan_features()
            self.scan_double()
        elif self.game.reflex.connected_rivet() == 2 and (mix1 not in [23,19,15,12,9,5]):
            self.scan_features()
            self.scan_double()
        elif self.game.reflex.connected_rivet() == 3 and (mix1 not in [1,5,6,7,9,12,13,15,18,19,23]):
            self.scan_features()
            self.scan_double()
        elif self.game.reflex.connected_rivet() == 4 and (mix1 in [2,3,4,8,10,11,14,16,17,22]):
            self.scan_features()
            self.scan_double()
        elif self.game.reflex.connected_rivet() == 5 and (mix1 in [2,4,8,10,11,14,16,22]):
            self.scan_features()
            self.scan_double()

    def scan_double(self):
        d = self.double_probability()

    def double_probability(self):
        sd = self.game.spotting.connected_rivet()
        mix3 = self.game.mixer3.connected_rivet()
        if self.game.card1_replay_counter.position == 0 or self.game.card2_replay_counter.position == 0 or self.game.card3_replay_counter.position == 0:
            #Check position of mixer3
            t = self.check_mixer_3()
            if t == 1:
                m = self.check_mixer_2()
                if m == 1:
                    if sd in [5,8,28,37,21,17]:
                        if self.game.c1_double.status == False:
                            self.game.c1_double.engage(self.game)
                            self.game.sound.play('tilt')
                    elif sd in [20,32,34,46,27,44]:
                        if self.game.c2_double.status == False:
                            self.game.c2_double.engage(self.game)
                            self.game.sound.play('tilt')
                    elif sd in [50,11,14,36,39,48]:
                        if self.game.c3_double.status == False:
                            self.game.c3_double.engage(self.game)
                            self.game.sound.play('tilt')


    def check_mixer_3(self):
        mix3 = self.game.mixer3.connected_rivet()
        if (mix3 in [2,5,6,8,11,12,14,16,17,20,22,24]):
            return 1
        elif (self.game.c1_double.status and (mix3 in [1,13,18,19])):
            return 1
        elif (self.game.c2_double.status and (mix3 in [9,10,13,21])):
            return 1
        elif (self.game.c3_double.status and (mix3 in [3,4,7,23])):
            return 1
        else:
            return 0

    def scan_features(self):
        p = self.features_probability()

    def features_probability(self):
        mix3 = self.game.mixer3.connected_rivet()
        if mix3 in [2,3,6,8,10,11,12,14,16,17,18,20,22,24]:
            self.check_trips()

    def check_trips(self):
        if self.game.selector.position == 3:
            if self.game.spotting.position in [2,9,18,38,13,22]:
                if self.game.selector.position == 3:
                    if 14 not in self.holes:
                        self.holes.append(14)
                        self.game.fourteen.engage(self.game)
                        self.game.sound.play('tilt')
            elif self.game.spotting.position in [1,24,42,47,4,31]:
                if self.game.selector.position == 3:
                    if 19 not in self.holes:
                        self.holes.append(19)
                        self.game.nineteen.engage(self.game)
                        self.game.sound.play('tilt')
            elif self.game.spotting.position in [6,13,30,40,12,25]:
                if self.game.selector.position == 3:
                    if 22 not in self.holes:
                        self.holes.append(22)
                        self.game.twentytwo.engage(self.game)
                        self.game.sound.play('tilt')
        if self.game.spotting.position in [10,3,29,19,26,45]:
            if self.game.corners.status == False:
                self.game.corners.engage(self.game)
                self.game.sound.play('tilt')
        elif self.game.spotting.position == 33:
            if 15 not in self.holes:
                self.holes.append(15)
                self.game.fifteen.engage(self.game)
                self.game.sound.play('tilt')
        elif self.game.spotting.position == 49:
            if 16 not in self.holes:
                self.holes.append(16)
                self.game.sixteen.engage(self.game)
                self.game.sound.play('tilt')
        elif self.game.spotting.position == 7:
            if 17 not in self.holes:
                self.holes.append(17)
                self.game.seventeen.engage(self.game)
                self.game.sound.play('tilt')
                
    def animate_both(self, args):
        start = args[0]
        diff = args[1]
        num = args[2]
        if start + num >= 50:
            start = 0
        if diff >= 0:
            num = num + 1
            graphics.miss_california.both_animation([self, start + num])
            self.cancel_delayed(name="display")
            diff = diff - 1
            args = [start,diff,num]
            self.delay(name="both_animation", delay=0.06, handler=self.animate_both, param=args)
        else:
            self.cancel_delayed(name="both_animation")
            self.delay(name="display", delay=0.1, handler=graphics.miss_california.display, param=self)
            self.scan_all()

    def check_mixer_2(self):
        mix2 = self.game.mixer2.connected_rivet()
        if ((mix2 in [5,7,9,10,11,12,17,18,20,21,22,24])):
            if mix2 == 24:
                return 0
            else:
                return 1
        else:
            return 0

    def check_spotted_numbers(self):
        mix2 = self.game.mixer2.connected_rivet()
        if (self.game.fourteen.status and self.game.fifteen.status and (mix2 in [1,2,6,15])):
            return 1
        elif (self.game.nineteen.status and self.game.sixteen.status and (mix2 in [3,8,14,16])):
            return 1
        elif (self.game.twentytwo.status and self.game.seventeen.status and (mix2 in [4,13,19,23])):
            return 1
        else:
            return 0
                    
    # Define reset as the knock-off, anti-cheat relay disabled, and replay reset enabled.  Motors turn while credits are knocked off.
    # When meter reaches zero and the zero limit switch is hit, turn off motor sound and leave backglass gi on, but with tilt displayed.

    def startup(self):        
        # Every bingo requires the meter to register '0' 
        # before allowing coin entry --
        # also needs to show a plain 'off' backglass.
        self.tilt_actions()

class MissCalifornia(procgame.game.BasicGame):
    """ Miss California was a reworked Atlantic City for the west coast """
    def __init__(self, machine_type):
        super(MissCalifornia, self).__init__(machine_type)
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
        self.mixer5 = units.Mixer("mixer5", 23)

        self.searchdisc = units.Search("searchdisc", 49)

        #Search relays
        self.s1 = units.Relay("s1")
        self.s2 = units.Relay("s2")
        self.s3 = units.Relay("s3")
        self.s4 = units.Relay("s4")
        self.s5 = units.Relay("s5")
        self.search_index = units.Relay("search_index")

        #Replay Counter
        self.card1_replay_counter = units.Stepper("card1_replay_counter", 200)
        self.card2_replay_counter = units.Stepper("card2_replay_counter", 200)
        self.card3_replay_counter = units.Stepper("card3_replay_counter", 200)
 
        #Corners Replay Counter
        self.corners_replay_counter = units.Stepper("corners_replay_counter", 200)

        #Initialize stepper units used to keep track of features or timing.
        self.timer = units.Stepper("timer", 40)
        self.ball_count = units.Stepper("ball_count", 8)

        # Initialize reflex(es) and mixers unique to this game
        self.reflex = units.Reflex("primary", 200)

        #Atlantic City has a combined EB/spotting disc, which I am calling
        #the spotting disc for convenience.
        self.spotting = units.Spotting("spotting", 50)

        #When engage()d, light 6v circuit, and enable game features, scoring,
        #etc. Disengage()d means that the machine is 'soft' tilted. 
        self.anti_cheat = units.Relay("anti_cheat")

        #Card score doubling trip relays
        self.c1_double = units.Relay("c1_double")
        self.c2_double = units.Relay("c2_double")
        self.c3_double = units.Relay("c3_double")

        #Selector keeps track of cards in play
        self.selector = units.Stepper("selector", 3)

        #When engage()d, spin.
        self.start = units.Relay("start")

        #Tilt is separate from anti-cheat in that the trip will move the shutter
        #when the game is tilted with 1st ball in the lane.  Also prevents you
        #from picking back up by killing the anti-cheat.  Can be engaged by 
        #tilt bob, slam tilt switches, or timer at 39th step.
        #Immediately kills motors.
        self.tilt = units.Relay("tilt")

        #Relay for corners lighting
        self.corners = units.Relay("corners")

        #Relays for spotted numbers
        self.sixteen = units.Relay("sixteen")
        self.fifteen = units.Relay("fifteen")
        self.fourteen = units.Relay("fourteen")
        self.nineteen = units.Relay("nineteen")
        self.seventeen = units.Relay("seventeen")
        self.twentytwo = units.Relay("twentytwo")

        self.replays = 0
        self.returned = False

    def reset(self):
        super(MissCalifornia, self).reset()
        self.logger = logging.getLogger('game')
        self.load_config('bingo.yaml')
        self.anti_cheat.engage(game)
        
        main_mode = MulticardBingo(self)
        self.modes.add(main_mode)
        
game = MissCalifornia(machine_type='pdb')
game.reset()
game.run_loop()
