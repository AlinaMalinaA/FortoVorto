from random import randint as rand

  
def load(fn):
  kom = open(fn,'r').read().split('\n')
  kom = kom[:-1]
  return kom

kom = load('nomgen/n_kom')
mid = load('nomgen/n_mid')
fin = load('nomgen/n_fin')
rep = []

def gen():
  def get():
    curn = kom[rand(0,len(kom)-1)]
    for i in range(rand(0,2)):
      curn += mid[rand(0,len(mid)-1)]
    curn += fin[rand(0,len(mid)-1)]
    return curn
  
  cur = get()
  while cur in rep:
    cur = get()
    pass
  rep.append(cur)
  return cur

def addkey(nam):
  rep.append(nam)
