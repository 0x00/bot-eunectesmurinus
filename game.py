import shelve

class Team:

        def __init__(self):
                self.name = "unknown"
                self.s = 0
                self.played = []
                self.w = 0, 0, 0, 0, 0, 0, 0, 0, 0

        def score(self):
                goal = 0
                fail = 0

                for m in self.played:
                        if m.active():
                                if m.team1==self:
                                        goal += m.goal1
                                        fail += m.goal2

                                if m.team2==self:
                                        goal += m.goal2
                                        fail += m.goal1

                return float(1+goal)/float(fail+1)

        def homeScore(self):
                goalHome = 0
                failHome = 0

                for m in self.played:
                        if m.team1==self and m.active():
                                goalHome += m.goal1
                                failHome += m.goal2

                return float(1+goalHome)/float(failHome+1)

        def medianHomeVictory(self):
                victories = []
                for m in self.played:
                        if m.active():
                                if m.team1==self and m.goal1>m.goal2:
                                        victories.append((m.goal1,m.goal2))

                if len(victories)==0: return (2,1)
                l = len(victories)/2                
                return victories[l]


        def medianAwayVictory(self):
                victories = []
                for m in self.played:
                        if m.active():
                                if m.team2==self and m.goal1<m.goal2:
                                        victories.append((m.goal1,m.goal2))
                if len(victories)==0: return (0,1)
                l = len(victories)/2
                return victories[l]


        def awayScore(self):

                goalAway = 0
                failAway = 0

                for m in self.played:
                        if m.team2==self and m.active():
                                goalAway += m.goal2
                                failAway += m.goal1

                return float(1+goalAway)/float(failAway+1)



class Match:

        def __init__(self, team1, team2,match_id,time,append=True):
                self.team1 = team1
                self.team2 = team2

                self.match_id = match_id

                self.goal1 = -1
                self.goal2 = -1

                self.time = time


                if append:
                        team1.played.append(self)
                        team2.played.append(self)

                        team1.played.sort(key=lambda m:m.time,reverse=False)
                        team2.played.sort(key=lambda m:m.time,reverse=False)
                        #print "appending match to "+team1.name+"/"+team2.name


        def active(self):
                return self.goal1!=-1 and self.goal2!=-1




        def pretty(self):
                import time
                d = time.localtime(self.time/1000)
                o =  "{team1:30} vs\t{team2:30} ({goal1}:{goal2}) \t@ {date}".format(team1=self.team1.name, team2=self.team2.name, goal1=self.goal1,goal2=self.goal2, date=str(d.tm_year)+"."+str(d.tm_mon)+"."+str(d.tm_mday)+" "+str(d.tm_hour)+":"+str(d.tm_min))
                return o


        def guess(self):

                so1 = 1
                so2 = 1


                s1 = self.team1.s
                s2 = self.team2.s

                if s1==0 or s2==0:
                        return (2,1)

                if s1>s2:
                        so1 = 2
                        so2 = 1
                        #return self.team1.medianHomeVictory()

                if s2>s1:
                        so2 = 1
                        so1 = 0
                        #return self.team2.medianAwayVictory()


                return (so1,so2)

        def update(self,w):

                if self.active():
                        if self.goal1>self.goal2:
                                self.team1.s = (1+self.team1.s)* w[0] + (self.team2.s)* w[4]#*self.team2.awayScore()
                                self.team2.s = (1+self.team2.s)* w[1] + (self.team1.s)* w[5]#*self.team1.homeScore()

                        if self.goal1<self.goal2:
                                self.team2.s = (1+self.team2.s)*w[2] + (self.team1.s)* w[6]#*self.team1.homeScore()
                                self.team1.s = (1+self.team1.s)*w[3] + (self.team2.s)* w[7]#*self.team2.awayScore()



class Game:

        def load(self):       
                d = shelve.open("gamedata")
                game = d["bl"]
                d.close()
                return game

        def save(self):
                d = shelve.open("gamedata")
                d["bl"] = self
                d.close()

        def __init__(self):
                self.teams = []
                self.links = {}
                self.matches = []
                self.w = 0, 0, 0, 0, 0, 0, 0, 0, 0

        def lookupTeam(self,name):
                team = False

                if not self.links.has_key(name):
                        team = Team()
                        team.name = name
                        self.links[name] = team
                        self.teams.append(team)
                        print "Creating new Team: #{name}#".format(name=name)

                return self.links[name]

                
