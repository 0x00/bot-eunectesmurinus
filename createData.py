import sys
import csv
from game import *
import shelve

filename = ""
if len(sys.argv[1:])>0:
        filename = sys.argv[1:][0]
else:
        filename = "./results.csv"

print "Filename is: "+filename

game = Game()

reader = csv.reader(open(filename, 'rb'), delimiter=';');
for r in reader:
	#print r
	team1 = game.lookupTeam(r[0])
	team2 = game.lookupTeam(r[1])

	goal = int(r[2])
	fail = int(r[3])

	time = long(r[6])
	matchId = int(r[5])

	match = Match(team1,team2,matchId,time)
	match.goal1 = goal
	match.goal2 = fail
	
	game.matches.append(match)


def time(match):
	return match.time
game.matches.sort(key=time)

def score(team):
	return team.score()
game.teams.sort(key=score,reverse=True)


d = shelve.open("gamedata")
d["bl"] = game
d.close()

for i in game.teams:
	print i.name+" "+str(i.goal)+" "+str(i.fail)+"  Score:"+str(i.score())

game.test()

