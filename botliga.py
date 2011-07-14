import httplib
import shelve
import sys
import csv
from game import Match

class Poster:

	token = False
	def toBotliga(self,mid, goal1, goal2):
		if(Poster.token):
			path = "/api/guess?match_id={mid}&result={goal1}:{goal2}&token={token}".format(mid=mid,token=Poster.token,goal1=goal1,goal2=goal2)
			con = httplib.HTTPConnection("botliga.de")
			con.request("POST", path)
			print con.getresponse().read();

        



post = Poster()

d = shelve.open("gamedata")
game = d["bl"]
d.close()

if len(sys.argv[1:])<1:
	print "I need a csv filename and a botliga auth token"
	sys.exit()

filename = sys.argv[1:][0]

if len(sys.argv[2:])==1:
	token = sys.argv[1:][1]
	Poster.token = token

print "Filename is: "+filename

reader = csv.reader(open(filename, 'rb'), delimiter=';');

for r in reader:

	team1 = game.lookupTeam(r[0])
	team2 = game.lookupTeam(r[1])

	time = long(r[6])
	matchId = int(r[5])

	match = Match(team1, team2, matchId, time,False)

	goal1 = match.guess()[0]
	goal2 = match.guess()[1]

	print "match id: {mid} \t guess: {goal1}:{goal2} \t {team1} vs. {team2}".format(team1=team1.name,team2=team2.name,mid=matchId,goal1=goal1,goal2=goal2)
	post.toBotliga(matchId,goal1,goal2)



