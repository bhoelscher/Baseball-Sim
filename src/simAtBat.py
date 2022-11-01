from simPitch import simPitch, PitchResult
import numpy as np
import constants as cn
import time
from Repository import Repository

class AtBatResult:
    def __init__(self, out, hit, walk, out_type, hit_type, contact_type, pitches):
        self.out = out
        self.hit = hit
        self.walk = walk
        self.out_type = out_type
        self.hit_type = hit_type
        self.contact_type = contact_type
        self.pitches = pitches

def simAtBat(game_id, batter, pitcher):
    repository = Repository()
    repository.updateCount(game_id, 0, 0)
    strikes = 0
    balls = 0
    pitches = 0
    outcome = False
    out = False
    hit = False
    walk = False
    out_type = None
    hit_type = None
    contact_type = None

    # Set Probablities for type of contact
    # Ground Ball min x, avg .44, max x
    ground_ball_perc = .44
    # Line Drive min x, avg .21, max x
    line_drive_perc = .21
    # Fly Ball min x, avg .35, max x
    fly_ball_perc = .35
    # Ground Ball batting average min x, avg .239, max x
    ground_ball_ba = .239
    # Line Drive batting average min x, avg .685, max x
    line_drive_ba = .685
    # Fly Ball batting average min x, avg .207, max x
    fly_ball_ba = .207
    # Line Drive Hit HR Chance avg .056
    ld_hr_chance = .056 + (batter.power - 70)/600
    # Line Drive Hit 2B chance avg .452
    ld_2b_chance = .452 + (batter.power - 70)/1200 + (batter.speed - 70)/300
    # Line Drive Hit 1B chance avg .492
    ld_1b_chance = .492 - (batter.power - 70)/400 - (batter.speed - 70)/300
    # Fly Ball HR chance avg .552
    fb_hr_chance = .552 + (batter.power - 70)/600
    # Fly Ball 3B chance avg .069
    fb_3b_chance = .069 + (batter.speed - 70)/600
    # Fly Ball 2B chance avg .207
    fb_2b_chance = .207 + (batter.power - 70)/1200 - (batter.speed - 70)/1200
    # Fly Ball 1B chance avg .172
    fb_1b_chance = .172 - (batter.power - 70)/400 - (batter.speed - 70)/1200
    # .10516
    # .14385, .008 HR, .065 2B
    # .07245, .04 HR, .015 2B, .005 3B

    # At-bat simulation loop
    while not outcome:
        pitch = simPitch(batter, pitcher)
        pitches += 1
        if not pitch.swing:
            # Pitch was taken, add a strike/ball to the count
            if pitch.strike:
                strikes += 1
            else:
                balls += 1
        elif not pitch.contact:
            # Swing and a miss, add a strike
            strikes += 1
        elif pitch.foul:
            # Foul ball, add a strike, but don't strikeout
            if strikes < 2:
                strikes += 1
        else:
            # Ball hit in play, determine outcome
            outcome = True
            contact_choices = [cn.GROUND_BALL, cn.LINE_DRIVE, cn.FLY_BALL]
            contact_chances = [ground_ball_perc, line_drive_perc, fly_ball_perc]
            contact_type = np.random.choice(contact_choices, p=contact_chances)
            #print("Hit in play")
            #print(contact_type)
            if contact_type == cn.GROUND_BALL:
                if ground_ball_ba > np.random.random():
                    hit = True
                    hit_type = cn.SINGLE
                    #print(cn.SINGLE)
                else:
                    out = True
                    out_type = cn.GROUND_OUT
                    #print("Ground out")
            elif contact_type == cn.LINE_DRIVE:
                if line_drive_ba > np.random.random():
                    hit = True
                    ld_hit_choices = [cn.SINGLE, cn.DOUBLE, cn.HOME_RUN]
                    ld_hit_chances = [ld_1b_chance, ld_2b_chance, ld_hr_chance]
                    hit_type = np.random.choice(ld_hit_choices, p=ld_hit_chances)
                    #print(hit_type)
                else:
                    out = True
                    out_type = cn.LINE_OUT
                    #print("Line out")
            else:
                if fly_ball_ba > np.random.random():
                    hit = True
                    fb_hit_choices = [cn.SINGLE, cn.DOUBLE, cn.TRIPLE, cn.HOME_RUN]
                    fb_hit_chances = [fb_1b_chance, fb_2b_chance, fb_3b_chance, fb_hr_chance]
                    hit_type = np.random.choice(fb_hit_choices, p=fb_hit_chances)
                    #print(hit_type)
                else:
                    out = True
                    out_type = cn.FLY_OUT
                    #print("Fly out")
        if strikes == 3:
            # Strikeout
            outcome = True
            out = True
            out_type = cn.STRIKEOUT
            #print("Strikeout")
        if balls == 4:
            # Walk
            outcome = True
            walk = True
            #print("Walk")
        repository.updateCount(game_id, balls, strikes)
        time.sleep(1)
        #if not outcome:
            #print(str(balls) + "-" + str(strikes))
    result = AtBatResult(out, hit, walk, out_type, hit_type, contact_type, pitches) 
    return result
