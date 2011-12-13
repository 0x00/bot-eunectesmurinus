import game
import kicktippsim

class Transition:
    def __init__(self):
      self.win_win = 0
      self.win_fail = 0
      self.fail_fail = 0
      self.fail_win = 0
      self.glob = 0

    def pretty(self):
        return "WW: {} WF:{} FF:{} FW:{}  All Transitions: {}".format(self.win_win,self.win_fail,self.fail_fail,self.fail_win,self.glob)

    def prettyP(self):
        return "WW: {} WF:{} FF:{} FW:{}".format(self.p(self.win_win),self.p(self.win_fail),self.p(self.fail_fail),self.p(self.fail_win))

    def p(self,e):
        return (e+1)/float(self.glob+4)


class MarkovChaingun:
   def lastWon(self,which="none"):
      def onlyActives(a):
          if a.active():
              if which=="none":
                  return True
              if which=="home" and a.team1==self.team:
                  return True
              if which=="out" and a.team2==self.team:
                  return True
          return False
      activegames = filter(onlyActives,self.team.played)
      lastgame = activegames[len(activegames)-1:][0]

      if lastgame.team1 == self.team and lastgame.goal1>lastgame.goal2:
                  return True
      if lastgame.team2 == self.team and lastgame.goal2>lastgame.goal1:        
                  return True
        
      return False
    
   def  __init__(self,team):
        self.ht = Transition()
        self.ot = Transition()

        self.homes = []
        self.outsides = []

        self.team= team

        for match in team.played:
            if match.active() and match.team1 ==  team:
                self.homes.append(match)
            
            if match.active() and match.team2 ==  team:
                self.outsides.append(match)
                
        #for match in self.homes:
            #print match.pretty()


        for index,item in enumerate(self.homes):
            if len(self.homes)>index+1:
               nextItem = self.homes[index+1]
               if item.goal1>item.goal2 and nextItem.goal1>nextItem.goal2:
                    self.ht.win_win +=1
               if item.goal1<=item.goal2 and nextItem.goal1<=nextItem.goal2:
                    self.ht.fail_fail +=1
               if item.goal1<=item.goal2 and nextItem.goal1>nextItem.goal2:
                    self.ht.fail_win +=1
               if item.goal1>item.goal2 and nextItem.goal1<=nextItem.goal2:
                    self.ht.win_fail +=1
               self.ht.glob+=1
               
        #for match in self.outsides:
            #print match.pretty()

        for index,item in enumerate(self.outsides):
            if len(self.outsides)>index+1:
               nextItem = self.outsides[index+1]
               if item.goal1<item.goal2 and nextItem.goal1<nextItem.goal2:
                    self.ot.win_win +=1
               if item.goal1>=item.goal2 and nextItem.goal1>=nextItem.goal2:
                    self.ot.fail_fail +=1
               if item.goal1>=item.goal2 and nextItem.goal1<nextItem.goal2:
                    self.ot.fail_win +=1
               if item.goal1<item.goal2 and nextItem.goal1>=nextItem.goal2:
                    self.ot.win_fail +=1
               self.ot.glob+=1
        
        #print self.ht.prettyP()
        #print self.ot.prettyP()
    
g = game.Game().load()

#for team in g.teams:
#    chain = MarkovChaingun(team)
#    print "---------"

sim = kicktippsim.KicktippSimulator()
highscore = 0
for match in g.matches:
    if match.active():
        print match.pretty()
        c1 = MarkovChaingun(match.team1)          
        c2 = MarkovChaingun(match.team2)
        #print match.team1.name, c1.lastWon("home"),c1.ht.prettyP()
        #print match.team2.name, c2.lastWon("out"),c2.ot.prettyP()

        tip = (0,0)
        d = 0
        a = 0
        b = 0

        if c1.lastWon("home") and c2.lastWon("out"):
            a = c1.ht.p(c1.ht.win_win)
            b = c2.ht.p(c2.ot.win_win)
            d = a-b
            print "win-win", d

        if c1.lastWon("home") and not c2.lastWon("out"):
            a = c1.ht.p(c1.ht.win_win)
            b = c2.ht.p(c2.ot.fail_win)
            d = a-b
            print "win-fail", d

        if not c1.lastWon("home") and c2.lastWon("out"):
            a = c1.ht.p(c1.ht.fail_win)
            b = c2.ht.p(c2.ot.win_win)
            d = a-b
            print "fail-win", d

        if not c1.lastWon("home") and not c2.lastWon("out"):
            a = c1.ht.p(c1.ht.fail_win)
            b = c2.ht.p(c2.ot.fail_win)
            d = a-b
            print "fail-fail", d
            
        if d>=0:
            tip = (round(2*a),round(1*b))
        else:
            tip = (0,1)

        score = sim.score(match,tip)
        print "score:",score,tip
        highscore +=score

print "total:",highscore
