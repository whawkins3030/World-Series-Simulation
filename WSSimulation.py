
# File: WSSimulation.py

# Name: Will Hawkins

# Date: January 10th, 2013

# This program simulates the Giants-Tigers World Series of 2012 by reading

# the batting statistics of each team and using probabilities to predict

# each team's winning percentage.


from WSPlayer import *

# Prompt for number of simulations. Initializes team rosters and game scores.
numSims = eval(input("How many World Series simulations shall we run? "))
giantsRoster = []
tigersRoster = []
giantsScore = [0]
tigersScore = [0]

# Creates the players and appends them to respective roster lists.
infileG = open('giants.dat', 'r')
infileT = open('tigers.dat', 'r')
lineG = infileG.readline()
lineT = infileT.readline()
while lineG != "" and lineT != "":
    g = lineG.split()
    t = lineT.split()
    playerG = WSPlayer(g[0], g[1], eval(g[2]), eval(g[3]), eval(g[4]), eval(g[5]), eval(g[6]), numSims, 'g')
    playerT = WSPlayer(t[0], t[1], eval(t[2]), eval(t[3]), eval(t[4]), eval(t[5]), eval(t[6]), numSims, 't')
    giantsRoster.append(playerG)
    tigersRoster.append(playerT)
    lineG = infileG.readline()
    lineT = infileT.readline()
infileG.close()
infileT.close()

# Initializes play-by-play for single-simulation calls.
if numSims == 1:
    outfile = open('wsplaybyplay.txt', 'w')
    playByPlay = True
    for player in giantsRoster+tigersRoster:
        player.initializeCounters()
else:
    outfile = open('wssimulations.txt', 'w')
    playByPlay = False


def main():

    # Initialize play-by-play text and 'team wins in X games' counters.
    if playByPlay:
        print("Giants-Tigers World Series Simulation", file=outfile)
        seriesRes = ""
    else:
        gWinsWithCount = [0,0,0,0]
        tWinsWithCount = [0,0,0,0]

    # Each series simulation consists of best of seven games.
    # Processes game winner, ends series when team wins four games.
    # Repeats 'numSims' times.
    for sim in range(1,numSims+1):
        gWCount = 0
        tWCount = 0
        
        for game in range(1,8):
            if playByPlay:
                print("\nGame " + str(game) + ":", file=outfile)
            winner = playOneGame()
            if winner == "g":
                gWCount += 1
                if playByPlay:
                    seriesRes += "Game "+str(game)+": Giants "+str(giantsScore[0])+" Tigers "+str(tigersScore[0])+"\n"
            elif winner == "t":
                tWCount += 1
                if playByPlay:
                    seriesRes += "Game "+str(game)+": Tigers "+str(tigersScore[0])+" Giants "+str(giantsScore[0])+"\n"

            # If team wins, process series winner and stop series.
            if gWCount >= 4 or tWCount >= 4:
                if gWCount > tWCount:
                    if playByPlay:
                        seriesRes += "\nGiants win the series " + str(gWCount) + "-" + str(tWCount)
                    else:
                        print(str(sim) + ": Giants win in " + str(game), file=outfile)
                        gWinsWithCount[game-4] += 1
                else:
                    if playByPlay:                        
                        seriesRes += "\nTigers win the series " + str(tWCount) + "-" + str(gWCount)
                    else:
                        print(str(sim) + ": Tigers win in " + str(game), file=outfile)
                        tWinsWithCount[game-4] += 1
                break


    # Prints results of the series simulation.
    if playByPlay:
        print("\nResults of World Series Simulation:\n")
        print(seriesRes)
        processStats()
    else:    
        print("\nResults of", numSims, "World Series Simulations:\n")
        print("Giants win in 7 - ", str(round(gWinsWithCount[3]/numSims*1000)/10), "%")
        print("Giants win in 6 - ", str(round(gWinsWithCount[2]/numSims*1000)/10), "%")
        print("Giants win in 5 - ", str(round(gWinsWithCount[1]/numSims*1000)/10), "%")
        print("Giants win in 4 - ", str(round(gWinsWithCount[0]/numSims*1000)/10), "%")
        print("Tigers win in 7 - ", str(round(tWinsWithCount[3]/numSims*1000)/10), "%")
        print("Tigers win in 6 - ", str(round(tWinsWithCount[2]/numSims*1000)/10), "%")
        print("Tigers win in 5 - ", str(round(tWinsWithCount[1]/numSims*1000)/10), "%")
        print("Tigers win in 4 - ", str(round(tWinsWithCount[0]/numSims*1000)/10), "%")
    outfile.close()



# Simulates one baseball game. Returns 'g' or 't' for winner.
def playOneGame():

    giantsScore[0] = 0
    tigersScore[0] = 0
    gCue = [0]
    tCue = [0]
    inning = 1

    # Main single-game loop. Overtime play if team is tied.
    while inning <= 9 or giantsScore[0] == tigersScore[0]:

        # Initializes the half-inning. Determines team roster and team cue.
        for team in ["giants", "tigers"]:
            if playByPlay:
                print("\nInning " + str(inning) + " - " + team.capitalize(), file=outfile)
            outCount = 0
            teamRoster = eval(team + "Roster")
            cue = eval(team[0] + "Cue")

            while outCount < 3:
                
                # Starts the team roster from last point (using the cue).
                for player in teamRoster[cue[0]:]+teamRoster[:cue[0]]:

                    # Sets player at bat, determines batting result, advances cue.
                    player.setBase(0)
                    hitRes = player.batting()
                    cue[0] += 1
                    if cue[0] > len(teamRoster) - 1:
                        cue[0] -= len(teamRoster)

                    # Processes batting result. If hit, advances bases and
                    # adds all dialog to play-by-play if needed.
                    if hitRes == 0:
                        player.setBase(-1)
                        if playByPlay:
                            print(player.getAbbName() + " was out.", file=outfile)
                        outCount += 1
                        if outCount >= 3: break
                    else:
                        swingText = ["singled", "doubled", "tripled", "homered"]                        
                        if playByPlay:
                            print(player.getAbbName() + " " + swingText[hitRes-1], end="", file=outfile) 
                            if hitRes != 1:
                                player.setStat(1, hitRes)
                        processHit(player, hitRes, teamRoster)

            for player in teamRoster:
                player.setBase(-1)

        if playByPlay:
            print("\nScore: Giants", giantsScore[0], "Tigers", tigersScore[0], file=outfile)
        inning += 1

    if giantsScore > tigersScore:
        return "g"
    else:
        return "t"


# Advances the players on base from the hitting result.
# Adds RBI stats to player at bat and updates team score.
def processHit(playerAtBat, hitRes, team):
    
    if playByPlay:
        rbiCount = 0
        scorers = []

    # For every player on the team, if they are on base
    # advance them by the magnitude of hit. Update team score.
    for player in team:
        if player.getBase() != -1:
            if player.getBase() + hitRes >= 4:
                if playByPlay:
                    scorers.append(player.getAbbName())
                    rbiCount += 1
                    player.setStat(1,1)
                player.setBase(-1)
                if player in giantsRoster: giantsScore[0] += 1
                else: tigersScore[0] += 1
            else:
                player.setBase(player.getBase() + hitRes)

    if playByPlay:
        playerAtBat.setStat(rbiCount, 0)
        if rbiCount > 0:
            print(" (" + ", ".join(scorers) + " scored).", file=outfile)
        else:
            print(".", file=outfile)


# Prints all single series statistics.
def processStats():
    
    # Initializes the 'list of lists' of RBI, Runs and Doubles leaders.
    statLeaders = [["", 0.0], ["", 0.0], ["", 0.0]]

    # Initializes the 'list of lists' of players scoring triples and homers.
    # Indexs: Giants triples (0), Giants homers (1), Tigers triples (2), Tigers homers (3)
    statLeaders2 = [[], [], [], []]

    # Calculates the stat leaders. Adds the players to the leaders
    # list if they have a greater (or equal) stat than the current leader. 
    for player in giantsRoster+tigersRoster:
        for j in [0, 1, 2]:
            if player.getStat(j) > statLeaders[j][1]:
                statLeaders[j][0] = player.getAbbName() + " (" + player.getTeam() + ")"
                statLeaders[j][1] = player.getStat(j)
            elif player.getStat(j) == statLeaders[j][1] and statLeaders[j][1] != 0.0:
                statLeaders[j][0] += ", " + player.getAbbName() + " (" + player.getTeam() + ")"
    for j in [3,4]:
        for player in giantsRoster:
            if player.getStat(j) > 0:
                statLeaders2[j-3].append(player)
        for player in tigersRoster:
            if player.getStat(j) > 0:
                statLeaders2[j-1].append(player)

    leaderTexts = ["\nRBI Leaders: ", "\nRuns Scored Leaders: ", "\nDoubles Leaders: ",
                   "\nTriples: ", "\nHome Runs: "]

    # Prints all Homers and Triples.
    for i in [4, 3]:
        print(leaderTexts[i] + "Giants - ", end="")
        text = ""
        for j in [i-3,i-1]:
            if statLeaders2[j]:
                for player in statLeaders2[j]:
                    text += player.getAbbName() + " " + str(player.getStat(i)) + ", "
                text = text[:-2] + " "
            else:
                text += "None "
            if j == i-3:
                text += " Tigers - "
        print(text)

    # Prints the Doubles, RBI, Runs leaders.
    for j in [2, 0, 1]:
        text = ""
        if statLeaders[j][0]:
            text += statLeaders[j][0] + " " + str(statLeaders[2][1])
        else:
            text += "None"
        print(leaderTexts[j] + text)



main()
