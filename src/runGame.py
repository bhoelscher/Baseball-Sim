from gameClasses import Pitcher, HittingGameStats, PitchingGameStats
from simGame import simGame
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

    awayTeam.pitcher = repository.getPitcher(awayTeamID)
    homeTeam.pitcher = repository.getPitcher(homeTeamID)

    awayTeam.batters = repository.getBatters(awayTeamID)
    homeTeam.batters = repository.getBatters(homeTeamID)

    gameResult = simGame(gameID, awayTeam, homeTeam)
    repository.logGameResult(gameID, awayTeamID, homeTeamID, gameResult)

    repository.logHittingStats(gameID, awayTeamID, gameResult.away_team)
    repository.logHittingStats(gameID, homeTeamID, gameResult.home_team)

    repository.logPitchingStats(gameID, awayTeamID, gameResult.away_team.pitcher)
    repository.logPitchingStats(gameID, homeTeamID, gameResult.home_team.pitcher)

    


runGame()
