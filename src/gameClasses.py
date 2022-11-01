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