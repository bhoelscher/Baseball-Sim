class ScoreBug extends HTMLElement {
    constructor() {
        super();
    }

    render() {
        this.innerHTML = null;
        this.createComponents();

        this.awayTeamName.innerHTML = this.getAttribute("awayteam");
        this.awayTeamScore.innerHTML = parseInt(this.getAttribute("awayscore"));
        this.homeTeamName.innerHTML = this.getAttribute("hometeam");
        this.homeTeamScore.innerHTML = parseInt(this.getAttribute("homescore"));
        this.inning.innerHTML = this.getAttribute("inning");
        this.ballsText.innerHTML = "Balls:";
        this.strikesText.innerHTML = "Strikes:";
        this.outsText.innerHTML = "Outs:";
        this.ballsCount.innerHTML = this.getAttribute("balls") ? parseInt(this.getAttribute("balls")) : 0;
        this.strikesCount.innerHTML = this.getAttribute("strikes") ? parseInt(this.getAttribute("strikes")) : 0 ;
        this.outsCount.innerHTML = this.getAttribute("outs") ? parseInt(this.getAttribute("outs")) : 0;
    }

    createComponents() {
        this.container = document.createElement("div");
        this.container.style = "height:200; width:450; background-color:#42813b; border:black; border-style:solid;";
        this.score = document.createElement("div");
        this.score.style = "display:inline-block; vertical-align:middle; height:200; align-items:center";
        this.inning = document.createElement("div");
        this.inning.style = "padding-left: 80px";

        this.teams = document.createElement("ul");
        this.teams.style = "list-style-type:none; width: 200px;";

        this.awayTeam = document.createElement("li");
        this.awayTeamName = document.createElement("div");
        this.awayTeamName.style = "display:inline-block; width: 150px";
        this.awayTeamScore = document.createElement("div");
        this.awayTeamScore.style = "display:inline-block";

        this.homeTeam = document.createElement("li");
        this.homeTeamName = document.createElement("div");
        this.homeTeamName.style = "display:inline-block; width: 150px";
        this.homeTeamScore = document.createElement("div");
        this.homeTeamScore.style = "display:inline-block";

        this.awayTeam.appendChild(this.awayTeamName);
        this.awayTeam.appendChild(this.awayTeamScore);
        this.homeTeam.appendChild(this.homeTeamName);
        this.homeTeam.appendChild(this.homeTeamScore);
        this.teams.appendChild(this.awayTeam);
        this.teams.appendChild(this.homeTeam);

        this.count = document.createElement("ul");
        this.count.style = "list-style-type:none; width: 100px;";

        this.balls = document.createElement("li");
        this.ballsText = document.createElement("div");
        this.ballsText.style = "display:inline-block; width: 75px";
        this.ballsCount = document.createElement("div");
        this.ballsCount.style = "display:inline-block";
        this.balls.appendChild(this.ballsText);
        this.balls.appendChild(this.ballsCount);

        this.strikes = document.createElement("li");
        this.strikesText = document.createElement("div");
        this.strikesText.style = "display:inline-block; width: 75px";
        this.strikesCount = document.createElement("div");
        this.strikesCount.style = "display:inline-block";
        this.strikes.appendChild(this.strikesText);
        this.strikes.appendChild(this.strikesCount);

        this.outs = document.createElement("li");
        this.outsText = document.createElement("div");
        this.outsText.style = "display:inline-block; width: 75px";
        this.outsCount = document.createElement("div");
        this.outsCount.style = "display:inline-block";
        this.outs.appendChild(this.outsText);
        this.outs.appendChild(this.outsCount);

        this.count.appendChild(this.balls);
        this.count.appendChild(this.strikes);
        this.count.appendChild(this.outs);

        this.score.appendChild(this.inning);
        this.score.appendChild(this.teams);
        this.score.appendChild(this.count);

        this.bases = document.createElement("div");
        this.bases.style = "list-style-type:none; width: 200px; display:inline-block; float:right";

        this.baseimg = document.createElement("img");
        this.baseimg.src = "assets/runners0.svg";
        this.baseimg.width = "200";
        this.baseimg.height = "200";

        this.bases.appendChild(this.baseimg);

        this.container.appendChild(this.score);
        this.container.appendChild(this.bases);
        
        this.appendChild(this.container);
    }

    connectedCallback() {
        this.render();
        this.updateGame("Shitty Team", 0, "The Cool Boys", 3, "Top 7th", 1, 2, 0, [false, true, true]);
    }

    updateGame(awayTeam, awayScore, homeTeam, homeScore, inning, balls, strikes, outs, bases) {
        this.awayTeamName.innerHTML = awayTeam;
        this.homeTeamName.innerHTML = homeTeam;
        this.updateScore(awayScore, homeScore);
        this.updateInning(inning);
        this.updateCount(balls, strikes, outs);
        this.updateRunners(bases);
    }

    updateScore(awayScore, homeScore) {
        this.awayTeamScore.innerHTML = awayScore;
        this.homeTeamScore.innerHTML = homeScore;
    }

    updateInning(inning) {
        this.inning.innerHTML = inning;
    }

    updateCount(balls, strikes, outs) {
        this.ballsCount.innerHTML = balls;
        this.strikesCount.innerHTML = strikes;
        this.outsCount.innerHTML = outs;
    }

    updateRunners(bases) {
        let baseCount = 0;
        if (bases[0]) baseCount += 1;
        if (bases[1]) baseCount += 2;
        if (bases[2]) baseCount += 4;
        console.log(baseCount);
        this.baseimg.src = `assets/runners${baseCount}.svg`;
    }
}

customElements.define("score-bug", ScoreBug);