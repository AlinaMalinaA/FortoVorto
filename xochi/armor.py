class Armor():
  """Armor of a Warrior"""

  def __init__(self):
    self.DC = 80 # Defence Chance, DC
    self.DP = 80 # Defence Potence, DP
    self.AV = 0 # Armor Value, AV
    self.EC = 100 # Evasion Chance
    pass

  def getEC(self):
    """Evasion Chance - Chance to halve incoming damage after sucessfull block"""
    return self.DP/self.DC * 100
 
