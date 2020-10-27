CREATE TABLE `teams` (
  `teamID` int NOT NULL AUTO_INCREMENT,
  `teamName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`teamID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `batters` (
  `playerID` int NOT NULL AUTO_INCREMENT,
  `playerName` varchar(45) DEFAULT NULL,
  `teamID` int DEFAULT NULL,
  `contact` int DEFAULT '0',
  `power` int DEFAULT '0',
  `speed` int DEFAULT '0',
  `vision` int DEFAULT '0',
  PRIMARY KEY (`playerID`),
  KEY `teams_idx` (`teamID`),
  CONSTRAINT `teams` FOREIGN KEY (`teamID`) REFERENCES `teams` (`teamID`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `pitchers` (
  `pitcherID` int NOT NULL AUTO_INCREMENT,
  `playerName` varchar(45) DEFAULT NULL,
  `teamID` int DEFAULT NULL,
  `control` int DEFAULT '0',
  `velocity` int DEFAULT '0',
  `movement` int DEFAULT '0',
  `stamina` int DEFAULT '0',
  PRIMARY KEY (`pitcherID`),
  KEY `teams_idx` (`teamID`),
  CONSTRAINT `pitcherteams` FOREIGN KEY (`teamID`) REFERENCES `teams` (`teamID`)
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

CREATE TABLE `hitting_stats` (
  `PlayerID` int NOT NULL,
  `TeamID` int NOT NULL,
  `GameID` int NOT NULL,
  `AtBats` int DEFAULT NULL,
  `Hits` int DEFAULT NULL,
  `Runs` int DEFAULT NULL,
  `RBIs` int DEFAULT NULL,
  `Walks` int DEFAULT NULL,
  `Strikeouts` int DEFAULT NULL,
  `Doubles` int DEFAULT NULL,
  `Triples` int DEFAULT NULL,
  `HomeRuns` int DEFAULT NULL,
  PRIMARY KEY (`PlayerID`,`TeamID`,`GameID`),
  KEY `team_idx` (`TeamID`),
  KEY `game_idx` (`GameID`),
  CONSTRAINT `game` FOREIGN KEY (`GameID`) REFERENCES `schedule` (`gameID`),
  CONSTRAINT `player` FOREIGN KEY (`PlayerID`) REFERENCES `batters` (`playerID`),
  CONSTRAINT `team` FOREIGN KEY (`TeamID`) REFERENCES `teams` (`teamID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `pitching_stats` (
  `PlayerID` int NOT NULL,
  `TeamID` int NOT NULL,
  `GameID` int NOT NULL,
  `Innings` float DEFAULT NULL,
  `EarnedRuns` int DEFAULT NULL,
  `Hits` int DEFAULT NULL,
  `Strikeouts` int DEFAULT NULL,
  `Walks` int DEFAULT NULL,
  `Pitches` int DEFAULT NULL,
  PRIMARY KEY (`PlayerID`,`TeamID`,`GameID`),
  KEY `gameP_idx` (`GameID`),
  KEY `teamP_idx` (`TeamID`),
  CONSTRAINT `gameP` FOREIGN KEY (`GameID`) REFERENCES `schedule` (`gameID`),
  CONSTRAINT `playerP` FOREIGN KEY (`PlayerID`) REFERENCES `pitchers` (`pitcherID`),
  CONSTRAINT `teamP` FOREIGN KEY (`TeamID`) REFERENCES `teams` (`teamID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;