from random import randint as rand

from armor import *
from weapon import *

class Char():
  """Common PRED profile for character"""

  def __init__(self,randum = 0, pts = 400,kfc = [0.25,0.25,0.25,0.25]):
    self.P = 100 #Power, ability to inflict damage
    self.R = 100 #Rate, ablity to make multiple strikes
    self.E = 100 #Endurance, ability to suffer, max Health
    self.D = 100 #Defence, ability to block shit
    self.H = 100 #Health, current Endurance potence
    self.Name = 'Sennoma'   #Tis Warruir hath no name
    self.I = 20             #Initiative
    self.armor = Armor()    #Armor of a Warrior
    self.weapon = Weapon()  #Weapon of Warrior

    self.rR = 0 #restR
    self.rD = 0 #restD
    
    self.mods = []          #Listo de modificacion

    self.statusoj = []      #Listo de Statusoj de Warrior

    self.pos_x = 0  #X Cord in a Cell
    self.pos_y = 0  #Y Cord in a Cell
    self.cell = None
    self.dead = False
    self.behavior = 'enemy'
    if pts != 400 or kfc!= [0.25,0.25,0.25,0.25]:
      self.R = self.c_par(0,pts*kfc[1],0)[0]
      self.P = self.c_par(0,pts*kfc[1],0)[1]+pts*kfc[0]
      self.D = self.c_par(0,pts*kfc[3],0)[0]
      self.E = self.c_par(0,pts*kfc[3],0)[1]+pts*kfc[2]
      self.H = self.E
 
    if randum > 0:
      a_part = rand(25, 75) * randum // 100
      v_part = randum - a_part
      r_part = rand(25, 50) * a_part // 100
      p_part = a_part - r_part
      d_part = rand(25, 50) * v_part // 100
      e_part = v_part - d_part
      rp = self.c_par(0,r_part,0)
      rd = self.c_par(0,d_part,0)
      self.R = rp[0]
      self.P = int(rp[1])+p_part
      self.rR = rp[1] - int(rp[1])
      self.D = rd[0]
      self.E = int(rd[1])+e_part
      self.rD = rd[1]- int(rd[1])
      self.H = self.E

  def raisePar(self,par,pts):
    if par=='P':
      self.P+=pts
    if par=='E':
      self.E+=pts
      self.H+=pts // 2
    if par=='D':
      self.D+=self.c_par(self.D,pts,self.rD)[0]
      self.rD=self.c_par(self.D,pts,self.rD)[1]
    if par=='R':
      self.R+=self.c_par(self.R,pts,self.rR)[0]
      self.rR=self.c_par(self.R,pts,self.rR)[1]


  def get_pts(self,val):
    if val <= 100:
      return val
    return val*val/100 - val + 100

  def get_dpts(self,base,val,rest):
    if val <= 100:
      return val-base
    return self.get_pts(val) - self.get_pts(base+rest)
 
  def is_alive(self):
    return self.H > 0
 
  def is_dead(self):
    return self.dead

  def die(self):
    self.dead = True

  def c_par(self,base,amount,rest):
    ret = [0,0]
    next = base+1
    while self.get_dpts(base, next, rest) <= amount:
      next+=1
      ret[0]+=1
    ret[1] = round(amount - self.get_dpts(base, next-1,rest),2)
    return ret


  def modu(self, parnam, parval):
    for mod in self.mods:
      if mod['TYPE'] == parnam+'_MUL':
        parval*= mod['VAL']
      if mod['TYPE'] == parnam+'_ADD':
        parval+= mod['VAL']
      if mod['TYPE'] == parnam+'_SET':
        parval = mod['VAL']
    return int(parval)

  def getA(self):
    """Attack: Ability attack potential of a char"""
    return self.P*self.R

  def getV(self):
    """Vitality: Ability to overcome damage"""
    return self.E*self.D
  

  def getH(self):
    """return H, even if it's modificated, like a shit!"""
    return self.modu('H',self.H)

  def getE(self):
    """return E, even if it's modificated, like a shit!"""
    return self.modu('E',self.E)

  def getP(self):
    """return P, even if it's modificated, like a shit!"""
    return self.modu('P',self.P)

  def getR(self):
    """return R, even if it's modificated, like a shit!"""
    return self.modu('R',self.R)

  def getD(self):
    """return D, even if it's modificated, like a shit!"""
    return self.modu('D',self.D)

  def getI(self):
    """return I, even if it's modificated, like a shit!"""
    return self.modu('I',self.I)

  def getStrikes(self):
    R = self.getR()
    if R % self.weapon.AR==0:
      return R // self.weapon.AR
    return R // self.weapon.AR + 1
  
  def getS_Chance(self):
    R = self.getR()
    if R % self.weapon.AR==0:
      return self.weapon.AC
    return (self.weapon.AC*(self.getStrikes()-1) + self.weapon.AC * ((R % self.weapon.AR) / self.weapon.AR)) // self.getStrikes()

  def getDodges(self):
    D = self.getD()
    if D % self.armor.DP==0:
      return D // self.armor.DP
    return D // self.armor.DP + 1
  
  def getD_Chance(self):
    D = self.getD()
    if D % self.armor.DP==0:
      return self.armor.DC
    return (self.armor.DC*(self.getDodges()-1) + self.armor.DC * ((D % self.armor.DP) / self.armor.DP)) // self.getDodges()
 
  def move(self,dir):
    """Change the position of a warrior in his excellent square"""
    nx = self.pos[0]+dir[0]
    ny = self.pos[1]+dir[1]
    if nx >= 0 and nx <= 2 and ny >= 0 and ny <=2:
      print('Dauras moving!')
      if self.cell.isfree(nx,ny):
        self.cell.free(self.pos[0],self.pos[1])
        self.cell.add(self,nx,ny)

  def flush_mods(self,type):
    """Option to destroy all modifiers of selected type, ekzemple, to use them unufoje!"""
    for mod in self.mods:
      if mod['T']==type:
         self.mods.remove(mod)
 
