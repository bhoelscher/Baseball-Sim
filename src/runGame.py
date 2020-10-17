from simGame import simGame, Pitcher, HittingGameStats, PitchingGameStats
from dbConnection import getConnection
from Repository import Repository
import mysql.connector



def runGame():
    repository = Repository()
    nextGame = repository.getNextGame()
    gameID = nextGame[0]
    awayTeamID = nextGame[1]
    homeTeamID = nextGame[2]

    awayTeam = repository.getTeam(awayTeamID)
    homeTeam = repository.getTeam(homeTeamID)

    awayTeam.pitcher = Pitcher("Carlos", 90, 70, 40, 70)
    homeTeam.pitcher = Pitcher("Marco", 70, 80, 90, 70)

    awayTeam.batters = repository.getBatters(awayTeamID)
    homeTeam.batters = repository.getBatters(homeTeamID)

    gameResult = simGame(awayTeam, homeTeam)
    repository.logGameResult(gameID, awayTeamID, homeTeamID, gameResult)

    repository.logHittingStats(gameID, awayTeamID, gameResult.away_team)
    repository.logHittingStats(gameID, homeTeamID, gameResult.home_team)

    


runGame()
