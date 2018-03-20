class Cell():
  """Cell sur batalkampo"""
  
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.kamp = [[None,None,None],[None,None,None],[None,None,None]]
    self.ckamp = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]

  def add(self, kio,x,y):
    """adds a mistvieho in a cell"""
    self.kamp[x][y] = kio
    self.ckamp[x][y] = kio.Name[0]
    kio.pos = [x,y]
    kio.cell = self
    
  def draw(self,bord=[]):
    """return an array of strings, that can be drawed like symbold"""
    ret = ['','','']
    n = 0
    if 'n' in bord:
      ret.append('')
      if 'w' in bord:
        ret[0] = ret[0]+'╔'
      ret[0] = ret[0]+'═══'
      if 'e' in bord:
        ret[0] =ret[0]+'╗'
      n = 1
    if 'w' in bord:
      ret[0+n] += '║'
      ret[1+n] += '║'
      ret[2+n] += '║'
    for i in range(3):
      for j in range(3):
        ret[j+n] = ret[j+n]+self.ckamp[i][j]
    if 'e' in bord:
      ret[0+n] += '║'
      ret[1+n] += '║'
      ret[2+n] += '║'
    if 's' in bord:
      ret.append('')
      if 'w' in bord:
        ret[3+n] = '╚'
      ret[3+n] += '═══'
      if 'e' in bord:
        ret[3+n] += '╝'
    return ret
  
  def isfree(self, x, y):
    """Check whether cell is free or not"""
    return self.kamp[x][y]==None
  
  def free(self, x, y):
    """Make the cell free!"""
    self.kamp[x][y] = None
    self.ckamp[x][y] = ' '
 
