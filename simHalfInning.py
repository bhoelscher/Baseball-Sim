from simAtBat import simAtBat
from random import random
import constants as cn
import time

class inningResult:
    def __init__(self, runs_scored, pitch_count, hits, next_hitter, lineup, pitcher):
        self.runs_scored = runs_scored
        self.pitch_count = pitch_count
        self.hits = hits
        self.next_hitter = next_hitter
        self.lineup = lineup
        self.pitcher = pitcher

def simHalfInning(score, lineup, current_hitter, pitcher):
    outs = 0
    pitch_count = 0
    runs_scored = 0
    hits = 0
    baserunners = [False, False, False]
    while outs < 3 and not (score.inning >=9 and (score.home_score + runs_scored) > score.away_score and not score.top):
        runs_scored_batter = 0
        batter = lineup[current_hitter]
        at_bat = simAtBat(batter, pitcher)
        pitch_count += at_bat.pitches
        pitcher.stats.pitches += at_bat.pitches
        if at_bat.out:
            outs += 1
            pitcher.stats.outs += 1
            lineup[current_hitter].stats.at_bats += 1
            if at_bat.out_type == cn.STRIKEOUT:
                pitcher.stats.strikeouts += 1
                lineup[current_hitter].stats.strikeouts += 1
            print(batter.name + ": " + str(at_bat.out_type) + ", " + str(outs) + " outs")
        elif at_bat.hit:
            hits += 1
            pitcher.stats.hits += 1
            lineup[current_hitter].stats.hits += 1
            lineup[current_hitter].stats.at_bats += 1
            if at_bat.hit_type == cn.HOME_RUN:
                lineup[current_hitter].stats.home_runs += 1
                runs_scored_batter += 1
                for runner in baserunners:
                    if runner:
                        runs_scored_batter += 1
                baserunners = [False, False, False]
            elif at_bat.hit_type == cn.TRIPLE:
                lineup[current_hitter].stats.triples += 1
                for runner in baserunners:
                    if runner:
                        runs_scored_batter += 1
                baserunners = [False, False, True]
            elif at_bat.hit_type == cn.DOUBLE:
                lineup[current_hitter].stats.doubles += 1
                if baserunners[cn.THIRD_BASE]:
                    runs_scored_batter += 1
                    baserunners[cn.THIRD_BASE] = False
                if baserunners[cn.SECOND_BASE]:
                    runs_scored_batter += 1
                if baserunners[cn.FIRST_BASE]:
                    # 43.3% average chance to score from first
                    score_chance = 0.433
                    if score_chance > random():
                        runs_scored_batter += 1
                        baserunners[cn.FIRST_BASE] = False
                    else:
                        baserunners[cn.THIRD_BASE] = True
                        baserunners[cn.FIRST_BASE] = False
                baserunners[cn.SECOND_BASE] = True
            elif at_bat.hit_type == cn.SINGLE:
                if baserunners[cn.THIRD_BASE]:
                    runs_scored_batter += 1
                    baserunners[cn.THIRD_BASE] = False
                if baserunners[cn.SECOND_BASE]:
                    # 58.8% average chance to score from second
                    score_chance = 0.588
                    if score_chance > random():
                        runs_scored_batter += 1
                        baserunners[cn.SECOND_BASE] = False
                        if baserunners[cn.FIRST_BASE]:
                            # 70% average chance to advance to third if runner scores from second
                            advance_to_third_chance = 0.7
                            if advance_to_third_chance > random():
                                baserunners[cn.THIRD_BASE] = True
                            else:
                                baserunners[cn.SECOND_BASE] = True
                    else:
                        baserunners[cn.THIRD_BASE] = True
                        baserunners[cn.SECOND_BASE] = baserunners[cn.FIRST_BASE]
                elif baserunners[cn.FIRST_BASE]:
                    # 21.1% average chance to advance to third with no runner on second
                    advance_to_third_chance = .211
                    if advance_to_third_chance > random():
                        baserunners[cn.THIRD_BASE] = True
                    else:
                        baserunners[cn.SECOND_BASE] = True
                baserunners[cn.FIRST_BASE] = True
            baserunner_string = "runners on: "
            if baserunners[cn.FIRST_BASE]:
                baserunner_string += "first "
            if baserunners[cn.SECOND_BASE]:
                baserunner_string += "second "
            if baserunners[cn.THIRD_BASE]:
                baserunner_string += "third "
            print(batter.name + ": " + str(at_bat.hit_type) + ", " + str(runs_scored_batter) + " RBIs. " + baserunner_string)
        elif at_bat.walk:
            lineup[current_hitter].stats.walks += 1
            pitcher.stats.walks += 1
            if baserunners[cn.FIRST_BASE]:
                if baserunners[cn.SECOND_BASE]:
                    if baserunners[cn.THIRD_BASE]:
                        runs_scored_batter += 1
                    baserunners[cn.THIRD_BASE] = True
                baserunners[cn.SECOND_BASE] = True
            baserunners[cn.FIRST_BASE] = True
            baserunner_string = "runners on: "
            if baserunners[cn.FIRST_BASE]:
                baserunner_string += "first "
            if baserunners[cn.SECOND_BASE]:
                baserunner_string += "second "
            if baserunners[cn.THIRD_BASE]:
                baserunner_string += "third "
            print(batter.name + ": " + "Walk "+ baserunner_string)
        lineup[current_hitter].stats.rbis += runs_scored_batter
        pitcher.stats.earned_runs += runs_scored_batter
        runs_scored += runs_scored_batter
        current_hitter += 1
        if current_hitter == len(lineup):
            current_hitter = 0
        #time.sleep(1)
    print("Inning over, " + str(runs_scored) + " runs scored on " + str(hits) + " hits. " + str(pitch_count) + " pitches thrown")
    result = inningResult(runs_scored, pitch_count, hits, current_hitter, lineup, pitcher)
    return result
