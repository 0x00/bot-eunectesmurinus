import botliga
from game import *
import time
import unicodedata

botreader = botliga.Reader()

game = Game()


def buildgamedb(jsonlink,game):
        json = botreader.read(jsonlink);
        for j in json:
                print j

                host = j["hostName"].replace(unichr(252),"ue").replace(unichr(228),"ae").replace(unichr(246),"oe")
                guest=  j["guestName"].replace(unichr(252),"ue").replace(unichr(228),"ae").replace(unichr(246),"oe")

                team1 = game.lookupTeam(host)
                team2 = game.lookupTeam(guest)

                
                goal = (j["hostGoals"])
                fail = (j["guestGoals"])
                if goal==None:
                        goal = -1
                if fail==None:
                        fail = -1
                

                timeObj = time.strptime((j["date"]).replace(".000Z",""), "%Y-%m-%dT%H:%M:%S")
                timestamp = long(time.mktime(timeObj)*1000)
                matchId = int(j["id"])

                match = Match(team1,team2,matchId,timestamp)
                match.goal1 = goal
                match.goal2 = fail
        
                game.matches.append(match)

        def timesort(match):
                return match.time
        game.matches.sort(key=timesort)

        def scoresort(team):
                return team.score()
        game.teams.sort(key=scoresort,reverse=True)




buildgamedb(botliga.Reader.s2010,game)
buildgamedb(botliga.Reader.s2011,game)

game.save()


for i in game.teams:
        print i.name+" Score:"+str(i.score())


print "Ok!"
