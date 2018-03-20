#!/usr/bin/python3
#coding=utf-8

#from random import randint as rand

from cell import *
from charo import *
from bqueue import *
from nomgen import *


def atako(anto,ato):
  """Default attack of a mistvieho"""
  ret = {}
  strajkoj = anto.getStrikes()
  prec = anto.getS_Chance()
  dodgoj = ato.getDodges()
  dodge = ato.getD_Chance()
  armor= ato.armor.AV - anto.weapon.AP
  if armor < 0:
    armor = 0
  damage = anto.P * anto.weapon.getAM() - armor
  fin_damage = 0
  ret['DAMAGE'] = damage
  ret['STRIKE_COUNT'] = strajkoj
  ret['DODGE_COUNT'] = dodgoj
  ret['DODGE_CHANCE'] = dodge
  ret['ATTACK_CHANCE'] = prec
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
      k_list = [0.5,1,2]
      anto = ago['ANTO']
      ato = ago['ATO']
      if anto.cell.x > ato.cell.x:
        # print ('right to left!')
        # 'B' is special battle mod. it works only during one attack! It is the mods for range, ekzemple, mifrendo!
        anto.mods.append({'TYPE':"R_MUL",'VAL':k_list[2-anto.pos[0]],'T':'B'})
        anto.mods.append({'TYPE':"D_MUL",'VAL':k_list[anto.pos[0]],'T':'B'})
        ato.mods.append({'TYPE':"R_MUL",'VAL':k_list[ato.pos[0]],'T':'B'})
        ato.mods.append({'TYPE':"D_MUL",'VAL':k_list[2-ato.pos[0]],'T':'B'})
      if anto.cell.x < ato.cell.x:
        #print ('left to right!')
        anto.mods.append({'TYPE':"R_MUL",'VAL':k_list[anto.pos[0]],'T':'B'})
        anto.mods.append({'TYPE':"D_MUL",'VAL':k_list[2-anto.pos[0]],'T':'B'})
        ato.mods.append({'TYPE':"R_MUL",'VAL':k_list[2-ato.pos[0]],'T':'B'})
        ato.mods.append({'TYPE':"D_MUL",'VAL':k_list[ato.pos[0]],'T':'B'})
      stat =  atako(anto,ato)
      #print (stat)
      anto.flush_mods('B')
      bq.add({'TYPE':'GET_DAMAGE', 'TTL':0, 'ID':ago['ATO'].Name, 'SRC':ago['ANTO'].Name,'VAL':stat['ALL_DAMAGE']},0)
      ret = stat
    if ago["TYPE"] == 'SUFFER':
      dmg = ago["VAL"]
      for mod in ago["CEL"].mods:
        if mod["TYPE"] == "DEFENSE":
          dmg = dmg // 2
      ago["CEL"].H -= dmg
      ret = dmg
    if ago["TYPE"] == 'DEFENSE':
      ago["ANTO"].mods.append({"TYPE":"DEFENSE","TTL":0,"T":"A"})
    return ret

def turno():
  """turnkontrolilo"""
 
  def getcel(listo,ink):
    k = 1
    for key in listo:
      if ink == key.lower() or ink== str(k):
        return (key)
      k+=1
    return listo[0]

  def spam_char(nomo,cell,inr = False, pts = 400, kfc = [0.25,0.25,0.25,0.25],ranpos = False):
    if inr:
      heraro[nomo] = Char(randum=inr)
    else:
      heraro[nomo] = Char(kfc=kfc,pts=pts)
    heraro[nomo].Name = nomo
    herlist.append(nomo)
    if ranpos:
      cell.add(heraro[nomo],rand(0,2),rand(0,2))
    else:
      cell.add(heraro[nomo],1,1)
    return heraro[nomo]
  
  def new_game():
    name = input('Ya name, yaoyopixqui?\n')
    if name=='r' or name == 'random':
      name = gen()
    else:
      addkey(name)
    role = ''
    ad = ''
    dd = ''
    while role not in ['1','2','3']:
      #0.4, 0.5, 0.6
      role = input("Select your battlerole:\n1)Punishmentizer\n2)Sentinel of Balance'\n3)Undestrictable\n")
    while ad not in ['1','2','3']:
      #0.4, 0.5, 0,6
      ad = input("Select your attack doctrine:\n1)Almighty\n2)DoubleChaired\n3)Furious Storm\n")
    while dd not in ['1','2','3']:
      dd = input("Select your defense stratagem:\n1)Boar from an army\n2)Cunny Boar\n3)Cunny Evader\n")
    kfc = [0,0,0,0]
    kfc[3] = round((int(role)*0.1+0.3)* (int(dd)*0.1+0.3),2)
    kfc[2] = round((int(role)*0.1+0.3)* (0.7 - int(dd)*0.1),2)
    kfc[1] = round((0.7 - int(role)*0.1)* (int(ad)*0.1+0.3),2)
    kfc[0] = round((0.7 - int(role)*0.1)* (0.7 - int(ad)*0.1),2)

    cellaro.clear()
    for i in range(3):
      cellaro.append([Cell(i,0),Cell(i,1),Cell(i,2)])
    herlist.clear()
    heraro.clear()
    nonlocal spiela,pts,mistpts,reslen,respts
    pts = 400
    mistpts = 100
    reslen =0
    respts = 0
    # print(kfc)
    spiela = spam_char(name,cellaro[1][1],kfc = kfc, pts = pts)
    spiela.behavior = 'human'
    spam_char(gen(),cellaro[1][0], inr = mistpts,ranpos = True)
    spam_char(gen(),cellaro[0][1], inr = mistpts,ranpos = True)
    spam_char(gen(),cellaro[1][2], inr = mistpts,ranpos = True)
    spam_char(gen(),cellaro[2][1], inr = mistpts,ranpos = True)
  
    global bq
    bq = BQueue()
 
    for c in herlist:
      bq.add({'TYPE':'HERO_TURN','TTL':0,'ID':c},0)
  
  cellaro = []
  herlist = []
  heraro = {}
  spiela = Char()
  pts = 0
  mistpts = 0
  reslen = 0
  respts = 0
  gamespeed = 10
  new_game()
  ans = ''
  while ans!= 'q':
    if not spiela.is_alive():
      print ("You have been defeated like a piece of defeateness!")
      print ("Your days on arena: %d. Your points of excellency: %d" % (reslen,respts // reslen))
      ans = input("What to do?\n")
      continue
    enemies = False
    for her in heraro.keys():
      if heraro[her].behavior=='enemy' and heraro[her].is_alive():
        enemies = True
    if not enemies:
      print("You Defeated Your enemies! Huei Tlatoani will try to sacrifice you anyway...")
      print("You have damn time to collect your strength, or to enhchance your power. What to do?")
      ans = input("1)Enhance Endurance\n2)Enhance Power\n3)Enhance Rate\n4)EnhanceDefence\n5Restire Half of Health\n")
      while ans not in ['1','2','3','4','5']:
        ans = input()
      if int(ans) < 5:
        dick = {'1':'E','2':'P','3':'R','4':'D'}
        spiela.raisePar(dick[ans],gamespeed)
      else:
        heal = (spiela.getE() - spiela.getH()) // 2
        print (heal,' dimage healed!')
        spiela.H+=heal
      reslen+=1
      respts+=mistpts*4
      mistpts+=gamespeed
      spam_char(gen(),cellaro[1][0], inr = mistpts,ranpos = True)
      spam_char(gen(),cellaro[0][1], inr = mistpts,ranpos = True)
      spam_char(gen(),cellaro[1][2], inr = mistpts,ranpos = True)
      spam_char(gen(),cellaro[2][1], inr = mistpts,ranpos = True)
    ev = bq.getnext()
    #print(ev)
    if ev['TYPE']=='HERO_TURN':
      cur = heraro[ev['ID']]
      if not cur.is_alive():
        pass
        #del heraro[cur]
      for mod in cur.mods:
        if mod['T']=='A':
          if mod['TTL']== 0:
            cur.mods.remove(mod)
          if mod['TTL']>0:
            mod['TTL']-=1
      if cur.behavior!='human':
        #Here AI lies like a mist of punishment!
        Agu([{'TYPE':'ATTACK','ANTO':heraro[cur.Name],'ATO':spiela}])
        print ("%s attacks %s!" % (cur.Name, spiela.Name))
        bq.add({'TYPE':'HERO_TURN', 'TTL':0, 'ID':cur.Name},cur.getI())
        continue 
      ret = True
      while ret:
        ans = input("Turno de " + cur.Name + "!What to do, mistvieh?\n")
        ans = ans.lower()
        arg = False
        args = []
        com = ans.split(' ')
        if len(com)>1:
          arg = True
          args = com[1:]
        if ans == 'q':
           ret = False
           break
        if com[0] == 'a' or com[0] =='attack':
          cel = None
          if arg:
            cel = heraro[getcel(herlist,args[0])]
          Agu([{'TYPE':'ATTACK','ANTO':heraro[cur.Name],'ATO':cel}])
          print ("%s attacks %s!" % (cur.Name, cel.Name))
          bq.add({'TYPE':'HERO_TURN', 'TTL':0, 'ID':cur.Name},cur.getI())
          ret = False
        elif ans == 'd' or ans == 'defense':
          Agu([{'TYPE':'DEFENSE','ANTO':heraro[cur.Name]}])
          print ("%s defences himself!" % (cur.Name))
          bq.add({'TYPE':'HERO_TURN', 'TTL':0, 'ID':cur.Name},cur.getI())
          ret = False
        elif ans == 'w' or ans == 'wait':
          print ("%s waits!" % (cur.Name))
          bq.add({'TYPE':'HERO_TURN', 'TTL':0, 'ID':cur.Name},cur.getI()//2)
          ret = False
        elif com[0] == 'l' or com[0] == 'list':
          #print(arg)
          if arg:
            her = heraro[getcel(herlist,args[0])]
            print ("%s:\nHealth: %d/%d\nPower: %d\nAttack Rate: %d + %f\nDefense Rate: %d + %f\n" % (her.Name,her.getH(),her.getE(),her.getP(),her.getR(),her.rR,her.getD(),her.rD))
          else:
            space = "---"
            print ("%s+%s+%s" % (space, space, space))
            for cell_row in cellaro:
              print ("%s|%s|%s" % (cell_row[0].draw()[0],cell_row[1].draw()[0],cell_row[2].draw()[0]))
              print ("%s|%s|%s" % (cell_row[0].draw()[1],cell_row[1].draw()[1],cell_row[2].draw()[1]))
              print ("%s|%s|%s" % (cell_row[0].draw()[2],cell_row[1].draw()[2],cell_row[2].draw()[2]))
              print ("%s+%s+%s" % (space, space, space))
            i = 1
            for key in herlist:
              print ("%d) %s (%d,%d)" % (i,key,heraro[key].cell.x,heraro[key].cell.y))
              i+=1
        elif com[0] =='m' or com[0] == 'move':
          if arg:
            dir = [0,0]
            if 'n' in com[1]:
              print('North!')
              dir[1] -= 1
            if 'e' in com[1]:
              print('East!')
              dir[0] += 1
            if 's' in com[1]:
              print('South!')
              dir[1] += 1
            if 'w' in com[1]:
              print('West!')
              dir[0] -= 1
            bq.add({'TYPE':'HERO_MOVE', 'TTL':0, 'ID':cur.Name,'DIR':dir},0)
            bq.add({'TYPE':'HERO_TURN', 'TTL':0, 'ID':cur.Name},cur.getI())
            ret = False
    elif ev['TYPE'] == 'HERO_MOVE':
      print(ev['DIR'])
      heraro[ev['ID']].move(ev['DIR'])
      
    elif ev['TYPE'] == 'GET_DAMAGE':
      dmg = Agu([{'TYPE':'SUFFER','CEL':heraro[ev['ID']],'SRC':heraro[ev['SRC']],'VAL':ev['VAL']}])
      print ("%d damage dealed to %s by %s!" % (dmg,ev['ID'],ev['SRC']))
    
    elif ev['TYPE'] == 'TURN_END':
      for h in herlist:
        if not heraro[h].is_alive() and not heraro[h].is_dead():
          print ('%s dies!' % heraro[h].Name)
          heraro[h].die()


if __name__ == '__main__':
  turno() 
