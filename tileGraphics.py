class colorPalette:
 def __init__(self,*args):
  self.colors=[]
  for a in args:
   self.colors.append(a)
 def get(self,index):
  return self.colors[index]
 def add(self,color):
  self.colors.append(color)

class sprite:
 def __init__(graphicsInstance,fileName):
  from PIL import Image as image
  im=image.open(fileName)
  rgb_im =im.convert("RGB")
# return rgb_im.getpixel((x,y))
  self.size=graphicsInstance.



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
 def put(self,x,y,colorIndex,width=1,height=1):
  for a in range(width):
   for b in range(height):
    self.matrix[y+b][x+a]=colorIndex
    pygame.draw.rect(screen,self.palette.get(colorIndex),((x+a)*self.tileWidth,(y+b)*self.tileWidth,self.tileWidth,self.tileWidth))
 def get(self,x,y):
  return self.matrix[y][x]
 def redraw(self):
  for a in range(self.width):
   for b in range(self.height):
    pygame.draw.rect(screen,self.palette.get(self.matrix[b][a]),((a)*self.tileWidth,(b)*self.tileWidth,self.tileWidth,self.tileWidth))
 def setName(self,name):
  pygame.display.set_caption(name)
 def fill(self,colorIndex):
  screen.fill(self.palette.get(colorIndex))
  for a in range(self.width):
   for b in range(self.height):
    self.matrix[b][a]=colorIndex
 def mouse(self):
  return pygame.mouse.get_pos()
 def mouseTile(self):
  pos=pygame.mouse.get_pos()
  x=pos[0]
  y=pos[1]
  x=int(x/self.tileWidth)
  y=int(y/self.tileWidth)
  return (x,y)
 def outline(self,color):
  for x in range(0,self.screenWidth+1,self.tileWidth):
   pygame.draw.line(screen,color,(x,0),(x,self.screenHeight))
  for y in range(0,self.screenHeight+1,self.tileWidth):
   pygame.draw.line(screen,color,(0,y),(self.screenWidth,y))
 def checkKey(self,key):
  return pygame.key.get_pressed()[key]==1
 def checkClick(self,button=0):
  return pygame.mouse.get_pressed()[button]==1
 def quit(self):
  pygame.quit()