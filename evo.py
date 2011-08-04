import botliga
import kicktippsim
from game import *

ksim = kicktippsim.KicktippSimulator()

print "Starting kicktipp season simulation.."
game = Game().load()
for i in game.teams:
        print "{:30} {}".format(i.name,i.score())


post = botliga.Poster()
ksim = kicktippsim.KicktippSimulator()


kicktipp=0
for g in game.matches:
  guess = g.guess()
  score = ksim.score(g, guess)
  kicktipp += score
  if g.active():
    print g.pretty()+" guessing... {} Kicktipp.de points:{}".format(guess,score)
  g.update(game.w[1:])
  post.toBotliga(g.match_id,guess[0],guess[1])

print kicktipp



