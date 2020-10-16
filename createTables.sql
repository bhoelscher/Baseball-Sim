CREATE TABLE `teams` (
  `teamID` int NOT NULL AUTO_INCREMENT,
  `teamName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`teamID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `players` (
  `playerID` int NOT NULL AUTO_INCREMENT,
  `playerName` varchar(45) DEFAULT NULL,
  `teamID` int DEFAULT NULL,
  PRIMARY KEY (`playerID`),
  KEY `teams_idx` (`teamID`),
  CONSTRAINT `teams` FOREIGN KEY (`teamID`) REFERENCES `teams` (`teamID`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `schedule` (
  `gameID` int NOT NULL AUTO_INCREMENT,
  `awayTeamID` int DEFAULT NULL,
  `homeTeamID` int DEFAULT NULL,
  `awayScore` int DEFAULT NULL,
  `homeScore` int DEFAULT NULL,
  `winningTeamID` int DEFAULT NULL,
  `losingTeamID` int DEFAULT NULL,
  `innings` int DEFAULT NULL,
  PRIMARY KEY (`gameID`),
  KEY `awayteam_idx` (`awayTeamID`),
  KEY `hometeam_idx` (`homeTeamID`),
  KEY `winner_idx` (`winningTeamID`),
  KEY `loser_idx` (`losingTeamID`),
  CONSTRAINT `awayteam` FOREIGN KEY (`awayTeamID`) REFERENCES `teams` (`teamID`),
  CONSTRAINT `hometeam` FOREIGN KEY (`homeTeamID`) REFERENCES `teams` (`teamID`),
  CONSTRAINT `loser` FOREIGN KEY (`losingTeamID`) REFERENCES `teams` (`teamID`),
  CONSTRAINT `winner` FOREIGN KEY (`winningTeamID`) REFERENCES `teams` (`teamID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;