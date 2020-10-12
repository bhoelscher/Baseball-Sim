from simHalfInning import simHalfInning

class CurrentScore:
    def __init__(self, away_score, home_score, inning, top):
        self.away_score = away_score
        self.home_score = home_score
        self.inning = inning
        self.top = top

class Team:
    def __init__(self, name, batters, pitcher):
        self.name = name
        self.batters = batters
        self.pitcher = pitcher
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

class Batter:
    def __init__(self, name, contact, power, speed, vision):
        self.name = name
        self.contact = contact
        self.power = power
        self.speed = speed
        self.vision = vision
        self.stats = HittingGameStats()

class Pitcher:
    def __init__(self, name, control, velocity, movement, stamina):
        self.name = name
        self.control = control
        self.velocity = velocity
        self.movement = movement
        self.stamina = stamina
        self.stats = PitchingGameStats()

class GameResult:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team

def simGame(away_team, home_team):
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
        inning += 1
    print("Final Score: " + away_team.name + ": " + str(away_score) + ", " + home_team.name + ": " + str(home_score))
    print(away_team.name + ": " + str(away_hits) + " hits and " + str(away_pitches) + " pitches")
    print(home_team.name + ": " + str(home_hits) + " hits and " + str(home_pitches) + " pitches")
    result = GameResult(home_team, away_team)
    return result

batter1 = Batter("Ted", 70, 70, 70, 70)
batter2 = Batter("Gregory", 80, 50, 80, 80)
batter3 = Batter("Melvin", 50, 90, 60, 70)
batter4 = Batter("Tim", 50, 50, 50, 50)
batter5 = Batter("Nick", 90, 90, 90, 90)
batter6 = Batter("Pat", 65, 80, 75, 80)
batter7 = Batter("Mark", 85, 70, 65, 80)
batter8 = Batter("Roberto", 60, 50, 70, 50)
batter9 = Batter("Diego", 75, 40, 70, 80)

batterh1 = Batter("Ted", 70, 70, 70, 70)
batterh2 = Batter("Gregory", 80, 50, 80, 80)
batterh3 = Batter("Melvin", 50, 90, 60, 70)
batterh4 = Batter("Tim", 50, 50, 50, 50)
batterh5 = Batter("Nick", 90, 90, 90, 90)
batterh6 = Batter("Pat", 65, 80, 75, 80)
batterh7 = Batter("Mark", 85, 70, 65, 80)
batterh8 = Batter("Roberto", 60, 50, 70, 50)
batterh9 = Batter("Diego", 75, 40, 70, 80)

pitcher1 = Pitcher("Carlos", 90, 70, 40, 70)
pitcher2 = Pitcher("Marco", 70, 80, 90, 70)

lineup = [batter1, batter2, batter3, batter4, batter5, batter6, batter7, batter8, batter9]
lineup2 = [batterh1, batterh2, batterh3, batterh4, batterh5, batterh6, batterh7, batterh8, batterh9]

home_team = Team("Chicago", lineup, pitcher1)
away_team = Team("New York", lineup2, pitcher2)

x = simGame(home_team, away_team)

