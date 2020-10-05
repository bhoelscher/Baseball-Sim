from simPitch import simPitch, PitchResult

def simAtBat():
    strikes = 0
    balls = 0
    outcome = False
    while not outcome:
        pitch = simPitch()
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
            print("Hit in play")
        if strikes == 3:
            outcome = True
            print("Strikeout")
        if balls ==4:
            outcome = True
            print("Walk")
        if not outcome:
            print(str(balls) + "-" + str(strikes))

simAtBat()
            
            
            
