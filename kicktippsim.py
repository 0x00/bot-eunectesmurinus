class KicktippSimulator:

  def draw(self, game):
    if game.goal1 == game.goal2:
      return True

    return False

  def diff(self,game):
    return game.goal1-game.goal2

  def home(self,game):
    return game.goal1>game.goal2

  def away(self,game):
    return game.goal1<game.goal2


  def score(self,game,guess):

    if not game.active():
      return 0

    score = 0
    if game.goal1==guess[0] and game.goal2==guess[1]:
      score = 5
    elif self.draw(game) and guess[0]==guess[1]:
      score = 2
    elif self.diff(game) == (guess[0]-guess[1]):
      score = 3
    elif self.home(game) and guess[0]>guess[1]:
      score = 2
    elif self.away(game) and guess[0]<guess[1]:
      score = 2

    return score
