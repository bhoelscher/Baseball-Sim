from simHalfInning import simHalfInning
from Repository import Repository
from gameClasses import CurrentScore, Team, HittingGameStats, PitchingGameStats, Batter, Pitcher, GameResult

def simGame(game_id, away_team, home_team):
    away_score = 0
    home_score = 0
    away_hits = 0
    home_hits = 0
    away_pitches = 0
    home_pitches = 0
    inning = 0
    top = True

    repository = Repository()
    repository.startGame(game_id)
 
    while inning < 9 or away_score == home_score:
        inning += 1
        top = True
        repository.updateInning(game_id, inning, 1 if top else 0)
        #print("Top of inning " + str(inning))
        score = CurrentScore(away_score, home_score, inning, top)
        top_half_result = simHalfInning(game_id, score, away_team.batters, away_team.next_hitter, home_team.pitcher)
        away_score += top_half_result.runs_scored
        away_hits += top_half_result.hits
        home_pitches += top_half_result.pitch_count
        away_team.next_hitter = top_half_result.next_hitter
        away_team.batters = top_half_result.lineup
        home_team.pitcher = top_half_result.pitcher
        #print(away_team + ": " + str(away_score) + ", " + home_team + ": " + str(home_score))
        if inning != 9 or home_score <= away_score:
            repository.updateInning(game_id, inning, 1 if top else 0)
            top = False
            #print("Bottom of inning " + str(inning))
            score = CurrentScore(away_score, home_score, inning, top)
            bottom_half_result = simHalfInning(game_id, score, home_team.batters, home_team.next_hitter, away_team.pitcher)
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