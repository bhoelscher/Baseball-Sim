from simGame import simGame, Team, Batter, Pitcher, HittingGameStats, PitchingGameStats
from dbConnection import getConnection
import mysql.connector

def getTeam(teamID):
    mydb = getConnection()
    cursor = mydb.cursor()
    getTeamQuery = 'SELECT * FROM baseball_test.teams where teamID = %s'
    cursor.execute(getTeamQuery, (str(teamID),))
    teamInfo = cursor.fetchone()
    team = Team(teamInfo[0], teamInfo[1])
    cursor.close()
    mydb.close()
    return team

def getBatters(teamID):
    mydb = getConnection()
    cursor = mydb.cursor()
    getBattersQuery = 'SELECT playerName FROM baseball_test.players where teamID = %s'
    cursor.execute(getBattersQuery, (str(teamID),))
    batterRows = cursor.fetchall()
    batters = []
    for x in batterRows:
        batter = Batter(x[0])
        batters.append(batter)
    cursor.close()
    mydb.close()
    return batters

def getNextGame():
    mydb = getConnection()
    cursor = mydb.cursor()
    cursor.execute("SELECT gameID, awayTeamID, homeTeamID FROM baseball_test.schedule where winningTeamID is NULL LIMIT 1")
    nextGame = cursor.fetchone()
    cursor.close()
    mydb.close()
    return nextGame

def logGameResult(gameID, awayTeamID, homeTeamID, gameResult):
    mydb = getConnection()
    cursor = mydb.cursor()
    if gameResult.home_score > gameResult.away_score:
        winner = homeTeamID
        loser = awayTeamID
    else:
        winner = awayTeamID
        loser = homeTeamID
    updateQuery = "UPDATE baseball_test.schedule SET awayScore = %s,homeScore = %s,winningTeamID =%s,losingTeamID = %s,innings = %s WHERE gameID = %s;"
    parameters = (gameResult.away_score, gameResult.home_score, winner, loser, gameResult.innings, gameID)
    cursor.execute(updateQuery, parameters)
    mydb.commit()
    cursor.close()
    mydb.close()
    


def runGame():

    nextGame = getNextGame()
    awayTeamID = nextGame[1]
    homeTeamID = nextGame[2]

    awayTeam = getTeam(awayTeamID)
    homeTeam = getTeam(homeTeamID)

    awayTeam.pitcher = Pitcher("Carlos", 90, 70, 40, 70)
    homeTeam.pitcher = Pitcher("Marco", 70, 80, 90, 70)

    awayTeam.batters = getBatters(awayTeamID)
    homeTeam.batters = getBatters(homeTeamID)

    gameResult = simGame(awayTeam, homeTeam)
    logGameResult(nextGame[0], awayTeamID, homeTeamID, gameResult)

    


runGame()
