class GymWrapper_LeekWarsFIght():

  def __init__(self):
    self.simulator = LeekWarsFight(...)


  def step(self, learnerAction) :
    turnEnded = learnerAction.do()
    if (turnEnded):
      currentPlayer = self.nextPlayer()
      while currentPlayer != learner):
        self.runPlayerTurn(currentPlayer)
    return observation, reward, terminated, truncated, info


  def reset(self) :
    self.simulator.resetfight()
