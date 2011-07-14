import shelve
import bpnn

d = shelve.open("gamedata")
game = d["bl"]
d.close()



class Timeline:

	lineSize = 4

	def __init__(self,team):
		self.team = team
		self.values = []
		

	def add(self,win,home):

		v = win,home
		self.values.append(v)

	def patternLine(self,start,end):
		p = []
		for a in self.values[start:end]:
			p.append(a[0])
			p.append(a[1])
		return p
	
	def buildPattern(self):
		amount = len(self.values)
		lines = []
		for i in range(amount-Timeline.lineSize-1):
			pattern = self.patternLine(i,Timeline.lineSize+i)
			lines.append([pattern, [self.values[i+Timeline.lineSize][0]]])
			print "{i}/{end}: {p} {t}".format(i=i,end=1+i+Timeline.lineSize,p=pattern,t=[self.values[i+Timeline.lineSize][0]])
			
		return lines

	def addMatchToTimeline(self,matches):
		print "adding match for {team} to timeline!".format(team=self.team.name)                                   
		for m in matches:
	
			if self.team == m.team1:
				win = 0
				print m.pretty()
				if m.goal1>m.goal2:
					win = min(1,m.goal1)
				self.add(win,1)
				       

			if self.team == m.team2:
				win = 0
				print m.pretty() 
				if m.goal2>m.goal1:
					win = min(1,m.goal2)
				self.add(win,0)
		
	def learn(self):
		print "learning...."
		pattern =  self.buildPattern()
		inputs = len(pattern[0][0])
		self.n = bpnn.NN(inputs,inputs,1)
		self.n.train(pattern)
		self.n.test(pattern)

	def visionize(self):
		last = len(self.values)
		actual = self.patternLine(last-Timeline.lineSize,last)[2:Timeline.lineSize*2] + [0,1]
		
		prediction = self.n.update(actual)
		print "the future for team {team} will be: {predict}".format(team=self.team.name, predict=prediction)
		return prediction
		


timeline = Timeline(game.teams[0])
timeline.addMatchToTimeline(game.matches)
timeline.learn()
timeline.visionize()

