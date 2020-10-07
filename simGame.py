from simHalfInning import simHalfInning

class currentScore:
    def __init__(self, away_score, home_score, inning, top):
        self.away_score = away_score
        self.home_score = home_score
        self.inning = inning
        self.top = top

def simGame():
    away_team = "Chicago"
    home_team = "New York"
    away_score = 0
    home_score = 0
    away_hits = 0
    home_hits = 0
    away_pitches = 0
    home_pitches = 0
    inning = 1
    top = True

    while inning <= 9 or away_score == home_score:
        top = True
        print("Top of inning " + str(inning))
        score = currentScore(away_score, home_score, inning, top)
        top_half_result = simHalfInning(score)
        away_score += top_half_result.runs_scored
        away_hits += top_half_result.hits
        home_pitches += top_half_result.pitch_count
        print(away_team + ": " + str(away_score) + ", " + home_team + ": " + str(home_score))
        if inning != 9 or home_score <= away_score:
            top = False
            print("Bottom of inning " + str(inning))
            score = currentScore(away_score, home_score, inning, top)
            bottom_half_result = simHalfInning(score)
            home_score += bottom_half_result.runs_scored
            home_hits += bottom_half_result.hits
            away_pitches += bottom_half_result.pitch_count
            print(away_team + ": " + str(away_score) + ", " + home_team + ": " + str(home_score))
        inning += 1
    print("Final Score: " + away_team + ": " + str(away_score) + ", " + home_team + ": " + str(home_score))
    print(away_team + ": " + str(away_hits) + " hits and " + str(away_pitches) + " pitches")
    print(home_team + ": " + str(home_hits) + " hits and " + str(home_pitches) + " pitches")

simGame()
