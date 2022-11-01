from simAtBat import simAtBat
from random import random
import constants as cn
import time
from Repository import Repository

class inningResult:
    def __init__(self, runs_scored, pitch_count, hits, next_hitter, lineup, pitcher):
        self.runs_scored = runs_scored
        self.pitch_count = pitch_count
        self.hits = hits
        self.next_hitter = next_hitter
        self.lineup = lineup
        self.pitcher = pitcher

def simHalfInning(game_id, score, lineup, current_hitter, pitcher):
    outs = 0
    pitch_count = 0
    runs_scored = 0
    hits = 0
    baserunners = [None, None, None]
    repository = Repository()

    # Half-inning sim loop. Half-inning ends with 3 outs, or the home team hitting a walk-off in the 9th or later
    while outs < 3 and not (score.inning >=9 and (score.home_score + runs_scored) > score.away_score and not score.top):
        runs_scored_batter = 0
        batter = lineup[current_hitter]
        at_bat = simAtBat(game_id, batter, pitcher)
        pitch_count += at_bat.pitches
        pitcher.stats.pitches += at_bat.pitches
        if at_bat.out:
            # Batter is out, add stats and continue to next batter
            #TODO: add logic to allow runners to advance on flyouts, groundouts, etc
            outs += 1
            pitcher.stats.outs += 1
            lineup[current_hitter].stats.at_bats += 1
            if at_bat.out_type == cn.STRIKEOUT:
                pitcher.stats.strikeouts += 1
                lineup[current_hitter].stats.strikeouts += 1
            print(batter.name + ": " + str(at_bat.out_type) + ", " + str(outs) + " outs")
        elif at_bat.hit:
            # Batter got a hit, advance runners appropriately and document stats
            hits += 1
            pitcher.stats.hits += 1
            lineup[current_hitter].stats.hits += 1
            lineup[current_hitter].stats.at_bats += 1
            if at_bat.hit_type == cn.HOME_RUN:
                # Home run, batter and all baserunners score
                lineup[current_hitter].stats.runs += 1
                lineup[current_hitter].stats.home_runs += 1
                runs_scored_batter += 1
                for runner in baserunners:
                    if runner is not None:
                        runs_scored_batter += 1
                        lineup[runner].stats.runs += 1
                baserunners = [None, None, None]
            elif at_bat.hit_type == cn.TRIPLE:
                # Triple, all baserunners score
                # Batter to third base
                lineup[current_hitter].stats.triples += 1
                for runner in baserunners:
                    if runner is not None:
                        runs_scored_batter += 1
                        lineup[runner].stats.runs += 1
                baserunners = [None, None, current_hitter]
            elif at_bat.hit_type == cn.DOUBLE:
                # Double, runners on second and third score
                # Runner on first advances to third with a chance of scoring,
                # Batter to second
                lineup[current_hitter].stats.doubles += 1
                if baserunners[cn.THIRD_BASE] is not None:
                    runs_scored_batter += 1
                    lineup[baserunners[cn.THIRD_BASE]].stats.runs += 1
                    baserunners[cn.THIRD_BASE] = None
                if baserunners[cn.SECOND_BASE] is not None:
                    runs_scored_batter += 1
                    lineup[baserunners[cn.SECOND_BASE]].stats.runs += 1
                if baserunners[cn.FIRST_BASE] is not None:
                    # 43.3% average chance to score from first
                    score_chance = 0.25 + .00708*lineup[baserunners[cn.FIRST_BASE]].speed - .000126*(lineup[baserunners[cn.FIRST_BASE]].speed**2) + .000000887*(lineup[baserunners[cn.FIRST_BASE]].speed**3)
                    if score_chance > random():
                        runs_scored_batter += 1
                        lineup[baserunners[cn.FIRST_BASE]].stats.runs += 1
                        baserunners[cn.FIRST_BASE] = None
                    else:
                        baserunners[cn.THIRD_BASE] = baserunners[cn.FIRST_BASE]
                        baserunners[cn.FIRST_BASE] = None
                baserunners[cn.SECOND_BASE] = current_hitter
            elif at_bat.hit_type == cn.SINGLE:
                # Single, runner on third scores
                # Runner on second to third, with a chance of scoring
                # Runner on first to second, with a chance of third if base is unoccupied
                # Batter to first
                if baserunners[cn.THIRD_BASE] is not None:
                    runs_scored_batter += 1
                    lineup[baserunners[cn.THIRD_BASE]].stats.runs += 1
                    baserunners[cn.THIRD_BASE] = None
                if baserunners[cn.SECOND_BASE] is not None:
                    # 58.8% average chance to score from second
                    score_chance = 0.35 + .00868*lineup[baserunners[cn.SECOND_BASE]].speed - .000141*(lineup[baserunners[cn.SECOND_BASE]].speed**2) + .000000926*(lineup[baserunners[cn.SECOND_BASE]].speed**3)
                    if score_chance > random():
                        runs_scored_batter += 1
                        lineup[baserunners[cn.SECOND_BASE]].stats.runs += 1
                        baserunners[cn.SECOND_BASE] = None
                        if baserunners[cn.FIRST_BASE] is not None:
                            # 70% average chance to advance to third if runner scores from second
                            advance_to_third_chance = 0.5 + .00763*lineup[baserunners[cn.FIRST_BASE]].speed - .000161*(lineup[baserunners[cn.FIRST_BASE]].speed**2) + .00000131*(lineup[baserunners[cn.FIRST_BASE]].speed**3)
                            if advance_to_third_chance > random():
                                baserunners[cn.THIRD_BASE] = baserunners[cn.FIRST_BASE]
                            else:
                                baserunners[cn.SECOND_BASE] = baserunners[cn.FIRST_BASE]
                    else:
                        baserunners[cn.THIRD_BASE] = baserunners[cn.SECOND_BASE]
                        baserunners[cn.SECOND_BASE] = baserunners[cn.FIRST_BASE]
                if baserunners[cn.FIRST_BASE] is not None and baserunners[cn.THIRD_BASE] is None:
                    # 21.1% average chance to advance to third if third base is empty
                    advance_to_third_chance = 0.05 + .0075*lineup[baserunners[cn.FIRST_BASE]].speed - .000158*(lineup[baserunners[cn.FIRST_BASE]].speed**2) + .00000118*(lineup[baserunners[cn.FIRST_BASE]].speed**3)
                    if advance_to_third_chance > random():
                        baserunners[cn.THIRD_BASE] = baserunners[cn.FIRST_BASE]
                    else:
                        baserunners[cn.SECOND_BASE] = baserunners[cn.FIRST_BASE]
                baserunners[cn.FIRST_BASE] = current_hitter
            baserunner_string = "runners on: "
            if baserunners[cn.FIRST_BASE] is not None:
                baserunner_string += "first "
            if baserunners[cn.SECOND_BASE] is not None:
                baserunner_string += "second "
            if baserunners[cn.THIRD_BASE] is not None:
                baserunner_string += "third "
            print(batter.name + ": " + str(at_bat.hit_type) + ", " + str(runs_scored_batter) + " RBIs. " + baserunner_string)
        elif at_bat.walk:
            # Batter walked, advance batter to first and any affected baserunners
            lineup[current_hitter].stats.walks += 1
            pitcher.stats.walks += 1
            if baserunners[cn.FIRST_BASE] is not None:
                if baserunners[cn.SECOND_BASE] is not None:
                    if baserunners[cn.THIRD_BASE] is not None:
                        runs_scored_batter += 1
                        lineup[baserunners[cn.THIRD_BASE]].stats.runs += 1
                    baserunners[cn.THIRD_BASE] = baserunners[cn.SECOND_BASE]
                baserunners[cn.SECOND_BASE] = baserunners[cn.FIRST_BASE]
            baserunners[cn.FIRST_BASE] = current_hitter
            baserunner_string = "runners on: "
            if baserunners[cn.FIRST_BASE] is not None:
                baserunner_string += "first "
            if baserunners[cn.SECOND_BASE] is not None:
                baserunner_string += "second "
            if baserunners[cn.THIRD_BASE] is not None:
                baserunner_string += "third "
            print(batter.name + ": " + "Walk "+ baserunner_string)
        lineup[current_hitter].stats.rbis += runs_scored_batter
        pitcher.stats.earned_runs += runs_scored_batter
        runs_scored += runs_scored_batter
        current_hitter += 1
        if current_hitter == len(lineup):
            current_hitter = 0
        homescore = score.home_score
        awayscore = score.away_score
        if score.top:
            awayscore += runs_scored
        else:
            homescore += runs_scored
        repository.updateAtBat(game_id, outs, baserunners, homescore, awayscore)
        #time.sleep(1)
    print("Inning over, " + str(runs_scored) + " runs scored on " + str(hits) + " hits. " + str(pitch_count) + " pitches thrown")
    result = inningResult(runs_scored, pitch_count, hits, current_hitter, lineup, pitcher)
    return result
