from simAtBat import simAtBat
import constants as cn

class inningResult:
    def __init__(self, runs_scored, pitch_count, hits):
        self.runs_scored = runs_scored
        self.pitch_count = pitch_count
        self.hits = hits

def simHalfInning(score):
    outs = 0
    pitch_count = 0
    runs_scored = 0
    hits = 0
    baserunners = [False, False, False]
    while outs < 3 and not (score.inning >=9 and (score.home_score + runs_scored) > score.away_score and not score.top):
        runs_scored_batter = 0
        at_bat = simAtBat()
        pitch_count += at_bat.pitches
        if at_bat.out:
            outs += 1
            print(str(at_bat.out_type) + ", " + str(outs) + " outs")
        elif at_bat.hit:
            hits += 1
            if at_bat.hit_type == cn.HOME_RUN:
                runs_scored_batter += 1
                for runner in baserunners:
                    if runner:
                        runs_scored_batter += 1
                baserunners = [False, False, False]
            elif at_bat.hit_type == cn.TRIPLE:
                for runner in baserunners:
                    if runner:
                        runs_scored_batter += 1
                baserunners = [False, False, True]
            elif at_bat.hit_type == cn.DOUBLE:
                if baserunners[cn.THIRD_BASE]:
                    runs_scored_batter += 1
                    baserunners[cn.THIRD_BASE] = False
                if baserunners[cn.SECOND_BASE]:
                    runs_scored_batter += 1
                if baserunners[cn.FIRST_BASE]:
                    baserunners[cn.THIRD_BASE] = True
                    baserunners[cn.FIRST_BASE] = False
                baserunners[cn.SECOND_BASE] = True
            elif at_bat.hit_type == cn.SINGLE:
                if baserunners[cn.THIRD_BASE]:
                    runs_scored_batter += 1
                baserunners[cn.THIRD_BASE] = baserunners[cn.SECOND_BASE]
                baserunners[cn.SECOND_BASE] = baserunners[cn.FIRST_BASE]
                baserunners[cn.FIRST_BASE] = True
            baserunner_string = "runners on: "
            if baserunners[cn.FIRST_BASE]:
                baserunner_string += "first "
            if baserunners[cn.SECOND_BASE]:
                baserunner_string += "second "
            if baserunners[cn.THIRD_BASE]:
                baserunner_string += "third "
            print(str(at_bat.hit_type) + ", " + str(runs_scored_batter) + " RBIs. " + baserunner_string)
        elif at_bat.walk:
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
            print("Walk "+ baserunner_string)
        runs_scored += runs_scored_batter
    print("Inning over, " + str(runs_scored) + " runs scored on " + str(hits) + " hits. " + str(pitch_count) + " pitches thrown")
    result = inningResult(runs_scored, pitch_count, hits)
    return result
