from simHalfInning import simHalfInning

class CurrentScore:
    def __init__(self, away_score, home_score, inning, top):
        self.away_score = away_score
        self.home_score = home_score
        self.inning = inning
        self.top = top

class Team:
   def __init__(self, teamID, name):
        self.teamID = teamID
        self.name = name
        self.next_hitter = 0

class HittingGameStats:
    at_bats = 0
    hits = 0
    runs = 0
    rbis = 0
    walks = 0
    strikeouts = 0
    doubles = 0
    triples = 0
    home_runs = 0

class PitchingGameStats:
    outs = 0
    earned_runs = 0
    hits = 0
    strikeouts = 0
    walks = 0
    pitches = 0

    def inningsPitched(self):
        innings = self.outs//3
        innings += (self.outs%3 / 10)
        return innings

class Batter:
    def __init__(self, player_id, name, contact, power, speed, vision):
        self.player_id = player_id
        self.name = name
        self.contact = contact
        self.power = power
        self.speed = speed
        self.vision = vision
        self.stats = HittingGameStats()

class Pitcher:
    def __init__(self, player_id, name, control, velocity, movement, stamina):
        self.player_id = player_id
        self.name = name
        self.control = control
        self.velocity = velocity
        self.movement = movement
        self.stamina = stamina
        self.stats = PitchingGameStats()

class GameResult:
    def __init__(self, home_team, away_team, home_score, away_score, innings):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.innings = innings

def simGame(away_team, home_team):
    away_score = 0
    home_score = 0
    away_hits = 0
    home_hits = 0
    away_pitches = 0
    home_pitches = 0
    inning = 0
    top = True
 
    while inning < 9 or away_score == home_score:
        inning += 1
        top = True
        #print("Top of inning " + str(inning))
        score = CurrentScore(away_score, home_score, inning, top)
        top_half_result = simHalfInning(score, away_team.batters, away_team.next_hitter, home_team.pitcher)
        away_score += top_half_result.runs_scored
        away_hits += top_half_result.hits
        home_pitches += top_half_result.pitch_count
        away_team.next_hitter = top_half_result.next_hitter
        away_team.batters = top_half_result.lineup
        home_team.pitcher = top_half_result.pitcher
        #print(away_team + ": " + str(away_score) + ", " + home_team + ": " + str(home_score))
        if inning != 9 or home_score <= away_score:
            top = False
            #print("Bottom of inning " + str(inning))
            score = CurrentScore(away_score, home_score, inning, top)
            bottom_half_result = simHalfInning(score, home_team.batters, home_team.next_hitter, away_team.pitcher)
            home_score += bottom_half_result.runs_scored
            home_hits += bottom_half_result.hits
            away_pitches += bottom_half_result.pitch_count
            home_team.next_hitter = bottom_half_result.next_hitter
            home_team.batters = bottom_half_result.lineup
            away_team.pitcher = bottom_half_result.pitcher
            #print(away_team + ": " + str(away_score) + ", " + home_team + ": " + str(home_score))
    print("Final Score: " + away_team.name + ": " + str(away_score) + ", " + home_team.name + ": " + str(home_score))
    print(away_team.name + ": " + str(away_hits) + " hits and " + str(away_pitches) + " pitches")
    print(home_team.name + ": " + str(home_hits) + " hits and " + str(home_pitches) + " pitches")
    result = GameResult(home_team, away_team, home_score, away_score, inning)
    return result