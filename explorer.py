import random
import sys

class Reweight:

        def __init__(self,game):
            self.kick_max=0
            self.game = game

        def getMaxForW(self,w):
                #print "{} {} {} {} {} {} {} {}".format(w1,w2,w3,w4,w11,w12,w13,w14)

                for t in self.game.teams:
                        t.s = 0
                          
                kicktipp = 0
                
                for g in self.game.matches:
                        guess = g.guess()
                        g.on = True
                        kicktipp += ksim.score(g,guess)

                        g.update(w)

                if kicktipp>self.kick_max:
                        self.kick_max=kicktipp
                        #print "kickmax: {},{}".format(self.kick_max,w)
                        sys.stdout.write("({})".format(kicktipp))

                return (kicktipp,)+w
                  

        def findViaDNA(self,initial=100,generations=30,childs=2,mutagen=2.5):
         def generatePop():
                p = []
                for i in range(initial):
                        e = (random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1))
                        ev = self.getMaxForW(e)
                        p.append(ev)
                return p
         def cross(a,b):
                 child = []
                 for i,e in enumerate(a):
                         child.append((0.5*e+0.5*b[i]))
                 return tuple(child)
         def mutate(a,factor=mutagen):
                child = list(a)
                i = random.randint(1,8)
                child[i] += random.uniform(-factor,factor)
                return tuple(child)
                 
         population = generatePop()
         
         def best(b1,b2,p):
                if p[0]>b1[0]:
                        b1 = p
                if p[0]>b2[0] and not p==b1:
                        b2 = p

                return (b1,b2)

         best1 = (0,0)
         best2 = (0,0)
         for p in population:
                 bs = best(best1,best2,p)
                 best1 = bs[0]
                 best2 = bs[1]
         g = 0
         while g < generations:
                 prototype = cross(best1,best2)
                 for i in range(childs):
                         m = mutate(prototype)
                         k = self.getMaxForW(m[1:])
                         #print "child: {}".format(k)
                         bs = best(best1,best2,k)
                         best1 = bs[0]
                         best2 = bs[1]
                 g+=1
                 if g%10==0:
                         sys.stdout.write(".")
                         
         if best1[0]>self.game.w[0]:
                 for t in self.game.teams:
                        t.s = 0
                 self.game.w = best1
                 self.game.save()


import kicktippsim
from game import *

ksim = kicktippsim.KicktippSimulator()
game = Game().load()
Reweight(game).findViaDNA(100,300,20,2)
