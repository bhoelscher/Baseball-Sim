from dbConnection import getConnection
from simGame import Batter, Team,  Pitcher
import mysql.connector

class Repository:
    mydb = getConnection()

    def getTeam(self, teamID):
        cursor = self.mydb.cursor()
        getTeamQuery = 'SELECT * FROM baseball_test.teams where teamID = %s'
        cursor.execute(getTeamQuery, (str(teamID),))
        teamInfo = cursor.fetchone()
        team = Team(teamInfo[0], teamInfo[1])
        cursor.close()
        return team

    def getBatters(self, teamID):
        cursor = self.mydb.cursor()
        getBattersQuery = 'SELECT playerID, playerName, contact, power, speed, vision FROM baseball_test.batters where teamID = %s'
        cursor.execute(getBattersQuery, (str(teamID),))
        batterRows = cursor.fetchall()
        batters = []
        for x in batterRows:
            batter = Batter(x[0], x[1], x[2], x[3], x[4], x[5])
            batters.append(batter)
        cursor.close()
        return batters

    def getPitcher(self, teamID):
        cursor = self.mydb.cursor()
        getPitcherQuery = 'SELECT pitcherID, playerName, control, velocity, movement, stamina FROM baseball_test.pitchers where teamID = %s limit 1'
        cursor.execute(getPitcherQuery, (str(teamID),))
        pitcherRow = cursor.fetchone()
        pitcher = Pitcher(pitcherRow[0], pitcherRow[1], pitcherRow[2], pitcherRow[3], pitcherRow[4], pitcherRow[5])
        cursor.close()
        return pitcher

    def getNextGame(self):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT gameID, awayTeamID, homeTeamID FROM baseball_test.schedule where winningTeamID is NULL LIMIT 1")
        nextGame = cursor.fetchone()
        cursor.close()
        return nextGame

    def logGameResult(self, gameID, awayTeamID, homeTeamID, gameResult):
        cursor = self.mydb.cursor()
        if gameResult.home_score > gameResult.away_score:
            winner = homeTeamID
            loser = awayTeamID
        else:
            winner = awayTeamID
            loser = homeTeamID
        updateQuery = "UPDATE baseball_test.schedule SET awayScore = %s,homeScore = %s,winningTeamID =%s,losingTeamID = %s,innings = %s WHERE gameID = %s;"
        parameters = (gameResult.away_score, gameResult.home_score, winner, loser, gameResult.innings, gameID)
        cursor.execute(updateQuery, parameters)
        self.mydb.commit()
        cursor.close()

    def logHittingStats(self, gameID, teamID, team):
        cursor = self.mydb.cursor()
        for player in team.batters:
            insertQuery = "INSERT INTO baseball_test.hitting_stats (PlayerID,TeamID,GameID,AtBats,Hits,Runs,RBIs,Walks,Strikeouts,Doubles,Triples,HomeRuns) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            parameters = (player.player_id, teamID, gameID, player.stats.at_bats, player.stats.hits, player.stats.runs, player.stats.rbis, player.stats.walks, player.stats.strikeouts, player.stats.doubles, player.stats.triples, player.stats.home_runs)
            cursor.execute(insertQuery, parameters)
        self.mydb.commit()
        cursor.close()

    def logPitchingStats(self, gameID, teamID, pitcher):
        cursor = self.mydb.cursor()
        insertQuery = "INSERT INTO `baseball_test`.`pitching_stats` (`PlayerID`,`TeamID`,`GameID`,`Innings`,`EarnedRuns`,`Hits`,`Strikeouts`,`Walks`,`Pitches`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        parameters = (pitcher.player_id, teamID, gameID, pitcher.stats.inningsPitched(), pitcher.stats.earned_runs, pitcher.stats.hits, pitcher.stats.strikeouts, pitcher.stats.walks, pitcher.stats.pitches)
        cursor.execute(insertQuery, parameters)
        self.mydb.commit()
        cursor.close()
