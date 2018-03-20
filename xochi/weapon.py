class Weapon():
  """Weapon of a Warrior"""

  def __init__(self):
    self.AC = 80 #Attack Chance, AC
    self.AR = 80 #Attack Rate, AR
    self.AP = 0 #Armor Piercing
    self.AD = 0 #Additional Damage
    self.PM = 1 #Power Modifier

  def getAM(self):
    """Atack Modifier - Power Modifier of each sucesfull strike"""
    return self.AR / self.AC


