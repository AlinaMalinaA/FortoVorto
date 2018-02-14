#!/usr/bin/python3
#coding=utf-8

class Char();
  """Common PRED profile for character"""

  def __init__(self):
    self.P = 0 #Power, ability to inflict damage
    self.R = 0 #Rate, ablity to make multiple strikes
    self.E = 0 #Endurance, ability to suffer, max Health
    self.D = 0 #Defence, ability to block shit
    self.H = 0 #Health, current Endurance potence
    self.armor = Armor()    #Armor of a Warrior
    self.weapon = Weapon()  #Weapon of Warrior

    self.statusoj = []      #Listo de Statusoj de Warrior

    self.pos_x = 0  #X Cord in a Cell
    self.pos_y = 0  #Y Cord in a Cell
    self.cell = Cell
    pass

  def getA(self):
    """Attack: Ability attack potential of a char"""
    return self.P*self.R

  def getV(self):
  """Vitality: Ability to overcome damage"""
    return self.E*self.D
  
class Armor():
  """Armor of a Warrior"""

  def __init__(self):
    self.DC = 0 # Defence Chance, DC
    self.DP = 0 # Defence Potence, DP
    self.AV = 0 # Armor Value, AV
    pass

  def getEC(self):
    """Evasion Chance - Chance to halve incoming damage after sucessfull block"""
    return self.DP/self.DC
   
class Weapon():
  """Weapon of a Warrior"""

  def __init__(self):
    self.AC = 0 #Attack Chance, AC
    self.AR = 0 #Attack Rate, AR
    self.AP = 0 #Armor Piercing
    self.AD = 0 #Additional Damage
    pass

  def getAM(self):
    """Atack Modifier - Power Modifier of each sucesfull strike"""
    return self.AR / self.AC

class Statuso():
  """Iu passivo shito"""
 
  def __init__(self):
    self.nomo = ''  #Nomo de statuso
    self.TTL = 0    #Kiel longo statuso vivas
    self.cTTL = 0   #Kiom da tempo restas
 
class Queue():
  """Battle Queue of events"""

  def __init__(self):
    self.que = [] #an array
  
  def add(self, kio, kien):
    """Add event or turn to a que"""
    pass

  def getnext(self):
    """return next event or event"""
    pass

class Cell():
  """Cell sur batalkampo"""
  
  def __init__(self)
    self.x = 0
    self.y = 0
    self.kamp = [[],[],[]]

def Ago():
  """Kium iu faras ion"""

  def ___init__(self)
    self.tipo = ''      #Tipo de ago - atako, defendo, e.t.c.
    self.subjekto = ''  #Kiu faras agon
    self.objektojn = [] #Kiu estas celo(j) de ago

  def agi(self)
    """fari tion, kio estas bezonata de ago.
    pass

def atako(anto, ato):
  """simpla atako - aux celita ago"""   
  pass

def defendo(anto):
  """simpla defendo - aux memcelita ago."""
  pass

def mov(anto, dir):
  """simpla movo en via celo"""
  pass

def turno():
  """turnkontrolilo"""
  pass


