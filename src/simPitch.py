from random import seed, random

class PitchResult:
    def __init__(self, strike, swing, contact, foul):
        self.strike = strike
        self.swing = swing
        self.contact = contact
        self.foul = foul

def simPitch(batter, pitcher):
    # strike percentage: min 48%, mean 62%, top 69%
    strike_perc = .397 + .00985*pitcher.control - .000163*(pitcher.control**2) + .000000962*(pitcher.control**3)
    # swing percentage at strike: min 53%, mean 65%, max 84%
    strike_swing_perc_batter = .452 + .00951*batter.vision - .000188*(batter.vision**2) + .00000132*(batter.vision**3)
    pitcher_mod = .15 - .00672*pitcher.movement + .000142*(pitcher.movement**2) - .0000011*(pitcher.movement**3)
    strike_swing_perc = strike_swing_perc_batter + pitcher_mod
    # swing percentage at balls: min 16%, mean 30%, max 45%
    ball_swing_perc_batter = .45 - .00737*batter.vision + .000145*(batter.vision**2) - .000000999*(batter.vision**3)
    pitcher_mod = -0.15 + .00739*pitcher.movement - .000159*(pitcher.movement**2) - .0000012*(pitcher.movemnt**3)
    # contact percentage at strike: min 72%, mean 87%, max 95%
    strike_contact_perc = .87
    # contact percentage at balls: min 42%, mean 65%, max 80%
    ball_contact_perc = .65
    # foul percentage: mean 50%
    foul_perc = .5

    strike = False
    swing = False
    contact = False
    foul = False
    
    seed()
    strike = strike_perc > random()

    if strike:
        swing = strike_swing_perc > random()
        if swing:
            contact = strike_contact_perc > random()
        else:
            contact = False
    else:
        swing = ball_swing_perc > random()
        if swing:
            contact = ball_contact_perc > random()
        else:
            contact = False

    if contact:
        foul = foul_perc > random()

##    if strike:
##        print("Strike")
##    else:
##        print("Ball")
##    if swing:
##        print("Swing")
##        if contact:
##            print("Hit")
##            if foul:
##                print("Foul")
##            else:
##                print("In play")
##        else:
##            print("Miss")
##    else:
##        print("Take")

    result = PitchResult(strike, swing, contact, foul)
    return result



    