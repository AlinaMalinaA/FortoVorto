import queue

class BQueue():
  """Battle Queue of events"""

  def __init__(self):
    #print ('BQueue created!')
    self.que = []
    self.curt = 0
    self.nque = queue.Queue()
    for i in range(20):
      self.que.append(queue.Queue())
    self.que[0].put({'TYPE':'BATTLE_START','TTL':0})
    self.que[0].put({'TYPE':'PLEN_TURN_START', 'TTL':0})
    self.que[0].put({'TYPE':'TURN_START', 'TTL':0, 'NUM':1})

  
  def add(self, kio, kien):
    """Add event or turn to a que"""
    if kien+self.curt >= 20:
      self.nque.put([kio,kien+self.curt-20])
    else:
      self.que[kien].put(kio)

  def getnext(self):
    """return next event or event"""
      
    if self.que[self.curt].qsize()==0:
      self.curt += 1
      ret = ({'TYPE':'TURN_END', 'TTL':0, 'NUM':self.curt})
      self.que[self.curt%20].put({'TYPE':'TURN_START', 'TTL':0, 'NUM':self.curt%20+1})
      if self.curt == 20:
        self.curt = 0 
        temp = self.que[0].get()
        self.que[0].put({'TYPE':'PLEN_TURN_START', 'TTL':0})
        self.que[0].put(temp)
        for i in range(self.nque.qsize()):
          c = self.nque.get()
          if c[1]>=20:
            c[1] = c[1]-20
            self.nque.put(c)
          else:
            self.que[c[1]].put(c[0])
      return(ret)
    event = self.que[self.curt].get()
    if event['TTL'] < 0:
      self.nque.put([event,self.curt])
    if event['TTL'] > 0:
      event['TTL'] -= 1
      self.nque.put([event,self.curt])
    return event


