class colorPalette:
 def __init__(self,*args):
  self.colors=[]
  for a in args:
   self.colors.append(a)
 def get(self,index):
  return self.colors[index]

class graphics:
 def __init__(self,width,height,palette="standard",roughSize=1000):
  if palette=="standard":
   palette=colorPalette((0,0,0),(0,0,255),(0,255,0),(0,255,255),(255,0,0),(255,0,255),(255,255,0),(255,255,255))
  temp1=int(roughSize/width)
  temp2=int(roughSize/height)
  self.tileWidth=temp1
  if temp2<temp1:
   self.tileWidth=temp2
  self.width=width
  self.height=height
  self.screenWidth=self.tileWidth*width
  self.screenHeight=self.tileWidth*height
  self.size=(self.screenWidth,self.screenHeight)
  global pygame,screen
  import pygame
  pygame.init()
  screen=pygame.display.set_mode(self.size)
  screen.fill(palette.get(0))
  self.matrix=[]
  self.palette=palette
  import copy
  temp=[]
  for x in range(width):
   temp.append(0)
  for y in range(height):
   self.matrix.append(copy.copy(temp))
 def update(self):
  pygame.event.get()
  pygame.display.flip()
 def put(self,x,y,colorIndex):
  self.matrix[y][x]=colorIndex
  pygame.draw.rect(screen,self.palette.get(colorIndex),(x*self.tileWidth,y*self.tileWidth,self.tileWidth,self.tileWidth))
 def get(self,x,y):
  return self.matrix[y][x]
 def setName(self,name):
  pygame.display.set_caption(name)