#!/usr/bin/python3
#coding=utf-8

import queue
from random import randint as rand

class Char():
  """Common PRED profile for character"""

  def __init__(self):
    self.P = 100 #Power, ability to inflict damage
    self.R = 100 #Rate, ablity to make multiple strikes
    self.E = 100 #Endurance, ability to suffer, max Health
    self.D = 100 #Defence, ability to block shit
    self.H = 100 #Health, current Endurance potence
    self.Name = 'Sennoma'   #Tis Warruir hath no name
    self.I = 20             #Initiative
    self.armor = Armor()    #Armor of a Warrior
    self.weapon = Weapon()  #Weapon of Warrior
    
    self.mods = []          #Listo de modificacion

    self.statusoj = []      #Listo de Statusoj de Warrior

    self.pos_x = 0  #X Cord in a Cell
    self.pos_y = 0  #Y Cord in a Cell
    self.cell = None
    pass

  def getA(self):
    """Attack: Ability attack potential of a char"""
    return self.P*self.R

  def getV(self):
    """Vitality: Ability to overcome damage"""
    return self.E*self.D

  def getStrikes(self):
    if self.R % self.weapon.AR==0:
      return self.R // self.weapon.AR
    return self.R // self.weapon.AR + 1
  
  def getS_Chance(self):
    if self.R % self.weapon.AR==0:
      return self.weapon.AC
    return self.weapon.AC*(self.getStrikes()-1) + self.weapon.AC * ((self.R % self.weapon.AR) / self.weapon.AR) // self.getStrikes()

  def getDodges(self):
    if self.D % self.armor.DP==0:
      return self.D // self.armor.DP
    return self.D // self.armor.DP + 1
  
  def getD_Chance(self):
    if self.D % self.armor.DP==0:
      return self.armor.DC
    return self.armor.DC*(self.getDodges()-1) + self.armor.DC * ((self.D % self.armor.DP) / self.armor.DP) // self.getDodges()
  
class Armor():
  """Armor of a Warrior"""

  def __init__(self):
    self.DC = 100 # Defence Chance, DC
    self.DP = 100 # Defence Potence, DP
    self.AV = 0 # Armor Value, AV
    self.EC = 100 # Evasion Chance
    pass

  def getEC(self):
    """Evasion Chance - Chance to halve incoming damage after sucessfull block"""
    return self.DP/self.DC * 100
   
class Weapon():
  """Weapon of a Warrior"""

  def __init__(self):
    self.AC = 100 #Attack Chance, AC
    self.AR = 100 #Attack Rate, AR
    self.AP = 0 #Armor Piercing
    self.AD = 0 #Additional Damage
    self.PM = 1 #Power Modifier
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
 
class BQueue():
  """Battle Queue of events"""

  def __init__(self):
    print ('BQueue created!')
    self.que = []
    self.curt = 0
    self.nque = queue.Queue()
    for i in range(20):
      self.que.append(queue.Queue())
    self.que[0].put({'TYPE':'BATTLE_START','TTL':0})
    self.que[0].put({'TYPE':'PLEN_TURN_START', 'TTL':-1})

  
  def add(self, kio, kien):
    """Add event or turn to a que"""
    if kien+self.curt >= 20:
      self.nque.put([kio,kien+self.curt-20])
    else:
      self.que[kien].put(kio)

  def getnext(self):
    """return next event or event"""
    while self.que[self.curt].qsize()==0:
      self.curt += 1
      if self.curt == 20:
        self.curt = 0 
        for i in range(self.nque.qsize()):
          c = self.nque.get()
          if c[1]>=20:
            c[1] = c[1]-20
            self.nque.put(c)
          else:
            self.que[c[1]].put(c[0])
    event = self.que[self.curt].get()
    if event['TTL'] < 0:
      self.nque.put([event,self.curt])
    if event['TTL'] > 0:
      event['TTL'] -= 1
      self.nque.put([event,self.curt])
    return event

class Cell():
  """Cell sur batalkampo"""
  
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.kamp = [[],[],[]]
 
def atako(anto,ato):
  """Default attack of a mistvieho"""
  ret = {}
  strajkoj = anto.getStrikes()
  prec = anto.getS_Chance()
  dodgoj = anto.getDodges()
  dodge = anto.getD_Chance()
  armor= ato.armor.AV - anto.weapon.AP
  if armor < 0:
    armor = 0
  damage = anto.P * anto.weapon.getAM() - armor
  fin_damage = 0
  ret['DAMAGE'] = damage
  ret['STRIKE_COUNT'] = strajkoj
  ret['ACC'] = prec
  ret['STRIKES'] = []
  ret['DODGES'] = []
  for s in range(strajkoj):
    r = rand(0,100)
    ret['STRIKES'].append({'roll':r})
    if r < prec:
      """Hit!"""
      dodge_st = []
      for d in range(dodgoj):
        r = rand(0,100)
        dodge_st.append({'roll':r})
        if r < dodge:
          """Dodge!"""
          damage -= armor
          e = ato.armor.getEC()
          mul=0
          while e >= 100:
            e-=100
            mul+=1
            damage = damage // 2
          if e > 0 and rand(0,100)<e:
            mul+=1
            damage = damage // 2
          dodge_st[-1]['mul'] = mul
      ret['DODGES'].append(dodge_st[:])
      fin_damage+=damage
      ret['STRIKES'][-1]['dmg'] = damage
    ret['ALL_DAMAGE'] = fin_damage
    return ret
           
def Agu(agaro):
  ret = 0
  for ago in agaro:
    if ago["TYPE"] == 'ATTACK':
      stat =  atako(ago['ANTO'],ago['ATO'])
      print (stat)
      bq.add({'TYPE':'GET_DAMAGE', 'TTL':0, 'ID':ago['ATO'].Name, 'SRC':ago['ANTO'].Name,'VAL':stat['ALL_DAMAGE']},0)
      ret = stat
    if ago["TYPE"] == 'GET_DAMAGE':
      dmg = ago["VAL"]
      for mod in ago["ANTO"].mods:
        if mod["TYPE"] == "DEFENSE":
          dmg = dmg // 2
      ago["CEL"].H -= dmg
      ret = dmg
    if ago["TYPE"] == 'DEFENSE':
      ago["ANTO"].mods.append({"TYPE":"DEFENSE","TTL":0,"T":"A"})
    return ret

def turno():
  """turnkontrolilo"""
  w_cell = Cell(0,0)
  e_cell = Cell(1,0)
  hero1 = Char()
  hero1.Name = "Mistborner"
  hero1.cell = w_cell
  hero1.pos = [1,1]
  hero2 = Char()
  hero2.Name = "Schmerzborner"
  hero2.cell = e_cell
  hero2.pos = [1,1]
  
  heraro = {}
  heraro[hero1.Name] = hero1
  heraro[hero2.Name] = hero2
  
  print ("Vi estas "+hero1.Name+", kaj vi nenion povas fari. Beadyrinde!")
  global bq
  bq = BQueue()
  bq.add({'TYPE':'HERO_TURN','TTL':0,'ID':hero1.Name},0)
  bq.add({'TYPE':'HERO_TURN','TTL':0,'ID':hero2.Name},0)
  ans = ''
  while ans!= 'q':
    ev = bq.getnext()
    print(ev)
    if ev['TYPE']=='HERO_TURN':
      cur = heraro[ev['ID']]
      for mod in cur.mods:
        if mod['T']=='A':
          if mod['TTL']== 0:
            cur.mods.remove(mod)
          if mod['TTL']>0:
            mod['TTL']-=1
      ans = input("Turno de " + cur.Name + "!What to do, mistvieh?\n")
      ans = ans.lower()
      if ans == 'a' or ans =='attack':
        Agu([{'TYPE':'ATTACK','ANTO':heraro[cur.Name],'ATO':heraro[cur.Name]}])
        print ("%s attacks %s!" % (cur.Name, cur.Name))
        bq.add({'TYPE':'HERO_TURN', 'TTL':0, 'ID':cur.Name},20)
      elif ans == 'd' or ans == 'defense':
        Agu([{'TYPE':'DEFENSE','ANTO':heraro[cur.Name]}])
        print ("%s defences himself!" % (cur.Name))
        bq.add({'TYPE':'HERO_TURN', 'TTL':0, 'ID':cur.Name},20)
      elif ans == 'w' or ans == 'wait':
        print ("%s waits!" % (cur.Name))
        bq.add({'TYPE':'HERO_TURN', 'TTL':0, 'ID':cur.Name},10)
      elif ans == 'l' or ans == 'list':
        print ("You know nothing!")
      else:
        bq.add({'TYPE':'HERO_TURN', 'TTL':0, 'ID':cur.Name},0)
    elif ev['TYPE'] == 'GET_DAMAGE':
      dmg = Agu([{'TYPE':'SUFFER','CEL':heraro[ev['ID']],'SRC':heraro[ev['SRC']],'VAL':ev['VAL']}])
      print ("%d damage dealed to %s by %s!" % (dmg,ev['ID'],ev['SRC']))
if __name__ == '__main__':
  turno() 
