import sys

class Team:

	def __init__(self):
		self.goal = 0
		self.goalHome = 0
		self.goalAway = 0

		self.fail = 0
		self.failHome = 0
		self.failAway = 0

		self.name = "unknown"

		self.neuromod = 1.4

		self.played = []

	def score(self):
		self.goal = 0
		self.fail = 0

		for m in self.played:
			if m.team1==self:
				self.goal += m.goal1
				self.fail += m.goal2
			
			if m.team2==self:
				self.goal += m.goal2
				self.fail += m.goal1

		return float(1+self.goal)/float(self.fail+1)

	def homeScore(self):
		self.goalHome = 0
		self.failHome = 0

		for m in self.played:
			if m.team1==self:
				self.goalHome += m.goal1
				self.failHome += m.goal2

		return float(1+self.goalHome)/float(self.failHome+1)


	def vsHomeScore(self, enemy):
		hit = 0
		fail = 0

		for m in self.played:
			if m.team1==self and m.team2==enemy:
				hit += m.goal1
				fail += m.goal2

		return float(1+hit)/float(1+fail)


	def vsAwayScore(self, enemy):
		hit = 0
		fail = 0

		for m in self.played:
			if m.team2==self and m.team1==enemy:
				hit += m.goal2
				fail += m.goal1

		return float(1+hit)/float(1+fail)



	def awayScore(self):

		self.goalAway = 0
		self.failAway = 0

		for m in self.played:
			if m.team2==self:
				self.goalAway += m.goal2
				self.failAway += m.goal1


		return float(1+self.goalAway)/float(self.failAway+1)



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


	def draw(self):

		if self.goal1 == self.goal2:
			return True

		return False

	def diff(self):
		return self.goal1-self.goal2

	def home(self):
		return self.goal1>self.goal2
	
	def away(self):
		return self.goal1<self.goal2





	def pretty(self):
		import time
		d = time.localtime(self.time/1000)
		o =  "{team1:30} vs\t{team2:30} ({goal1}:{goal2}) \t@ {date}".format(team1=self.team1.name, team2=self.team2.name, goal1=self.goal1,goal2=self.goal2, date=str(d.tm_year)+"."+str(d.tm_mon)+"."+str(d.tm_mday)+" "+str(d.tm_hour)+":"+str(d.tm_min))
		return o

		#return self.team1.name+" vs. "+self.team2.name+" "+str(self.goal1)+":"+str(self.goal2)+" @ "+str(d.tm_year)+"."+str(d.tm_mon)+"."+str(d.tm_mday)+" "+str(d.tm_hour)+":"+str(d.tm_min)


	def guess(self):
	
		#score1 = int(self.team1.homeScore()*self.team1.neuromod*self.team1.score()*self.team1.neuromod)
		#score2 = int(self.team2.awayScore()*self.team2.neuromod*self.team2.score()*self.team2.neuromod)
		#score1 = int(self.team1.homeScore()+self.team1.score())
		#score2 = int(self.team2.awayScore()+self.team2.score())
		score1 = int(self.team1.vsHomeScore(self.team2))
		score2 = int(self.team2.vsAwayScore(self.team1))


		return (min(4,score1),min(4,score2)) 


	def kicktippScore(self,guess):

		score = 0
		if self.goal1==guess[0] and self.goal2==guess[1]:
			score = 5
		elif self.draw() and guess[0]==guess[1]: 
			score = 2
		elif self.diff() == (guess[0]-guess[1]):
			score = 3
		elif self.home() and guess[0]>guess[1]:
			score = 2
		elif self.away() and guess[0]<guess[1]:
			score = 2


		return score



class Game:

	def __init__(self):
		self.teams = []
		self.links = {}
		self.matches = []

	def lookupTeam(self,name):
		team = False

		if not self.links.has_key(name):
			team = Team()
			team.name = name
			self.links[name] = team
			self.teams.append(team)
			print "Creating new Team: #{name}#".format(name=name)
		
		if self.links.has_key(name):
			team = self.links[name]

		return team


	def test(self):
		print "--------------------------------"

		kicktippMax = 0;
		kicktipp = 0
		
		for m in self.matches:
				guess = m.guess()
				kicktipp += m.kicktippScore(guess)
				kicktippMax+=5
				print m.pretty()+"  ::  guess:"+str(guess[0])+":"+str(guess[1])+" Kicktipp: "+str(m.kicktippScore(guess))
				#self.update(m.team1,m.goal1,m.goal2,True)
				#self.update(m.team2,m.goal2,m.goal1,False)

		for n in range(20):
			sys.stdout.write("- ")
		print

		print "Total kicktipp score: "+str(kicktipp)+ " Max: "+str(kicktippMax)

