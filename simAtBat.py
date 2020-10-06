from simPitch import simPitch, PitchResult
import numpy as np
import constants as cn

class AtBatResult:
    def __init__(self, out, hit, walk, out_type, hit_type, contact_type, pitches):
        self.out = out
        self.hit = hit
        self.walk = walk
        self.out_type = out_type
        self.hit_type = hit_type
        self.contact_type = contact_type
        self.pitches = pitches

def simAtBat():
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
    ld_hr_chance = .056
    # Line Drive Hit 2B chance avg .452
    ld_2b_chance = .452
    # Line Drive Hit 1B chance avg .492
    ld_1b_chance = .492
    # Fly Ball HR chance avg .552
    fb_hr_chance = .552
    # Fly Ball 3B chance avg .069
    fb_3b_chance = .069
    # Fly Ball 2B chance avg .207
    fb_2b_chance = .207
    # Fly Ball 1B chance avg .172
    fb_1b_chance = .172
    ground_ball = "GroundBall"
    line_drive = "LineDrive"
    fly_ball = "FlyBall"
    single = "Single"
    double = "Double"
    triple = "Triple"
    home_run = "Home Run"
    # .10516
    # .14385, .008 HR, .065 2B
    # .07245, .04 HR, .015 2B, .005 3B
    while not outcome:
        pitch = simPitch()
        pitches += 1
        if not pitch.swing:
            if pitch.strike:
                strikes += 1
            else:
                balls += 1
        elif not pitch.contact:
            strikes += 1
        elif pitch.foul:
            if strikes < 2:
                strikes += 1
        else:
            outcome = True
            contact_choices = [cn.GROUND_BALL, cn.LINE_DRIVE, cn.FLY_BALL]
            contact_chances = [ground_ball_perc, line_drive_perc, fly_ball_perc]
            contact_type = np.random.choice(contact_choices, p=contact_chances)
            #print("Hit in play")
            #print(contact_type)
            if contact_type == cn.GROUND_BALL:
                if ground_ball_ba > np.random.random():
                    hit = True
                    print(cn.SINGLE)
                else:
                    out = True
                    out_type = cn.GROUND_OUT
                    print("Ground out")
            elif contact_type == cn.LINE_DRIVE:
                if line_drive_ba > np.random.random():
                    hit = True
                    ld_hit_choices = [cn.SINGLE, cn.DOUBLE, cn.HOME_RUN]
                    ld_hit_chances = [ld_1b_chance, ld_2b_chance, ld_hr_chance]
                    hit_type = np.random.choice(ld_hit_choices, p=ld_hit_chances)
                    print(hit_type)
                else:
                    out = True
                    out_type = cn.LINE_OUT
                    print("Line out")
            else:
                if fly_ball_ba > np.random.random():
                    hit = True
                    fb_hit_choices = [cn.SINGLE, cn.DOUBLE, cn.TRIPLE, cn.HOME_RUN]
                    fb_hit_chances = [fb_1b_chance, fb_2b_chance, fb_3b_chance, fb_hr_chance]
                    hit_type = np.random.choice(fb_hit_choices, p=fb_hit_chances)
                    print(hit_type)
                else:
                    out = True
                    out_type = cn.FLY_OUT
                    print("Fly out")
        if strikes == 3:
            outcome = True
            out = True
            outType = cn.STRIKEOUT
            print("Strikeout")
        if balls ==4:
            outcome = True
            walk = True
            print("Walk")
        if not outcome:
            print(str(balls) + "-" + str(strikes))
    result = AtBatResult(out, hit, walk, out_type, hit_type, contact_type, pitches) 
    return result

simAtBat()
simAtBat()
simAtBat()
x = simAtBat()
            
            
            
