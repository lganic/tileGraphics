class spriteManager:
 def __init__(self,graphicsInstance,folder,backgroundColor=(-1,-1,-1)):
  import os
  self.data={}
  lst=os.listdir(folder)
  for a in lst:
   if a.endswith(".png"):
    self.data[a]=sprite(graphicsInstance,a,backgroundColor=backgroundColor,folder=folder)
 def get(self,name):
  if not name.endswith(".png"):
   name+=".png"
  return self.data[name]
 def getNames(self):
  return list(self.data.keys())

class complexSpriteManager:
 def __init__(self,graphicsInstance,folder,backgroundColor=(-1,-1,-1)):
  import os
  self.data={}
  lst=os.listdir(folder)
  for a in lst:
   if a.endswith(".cplx"):
    self.data[a]=complexSprite(graphicsInstance,folder,backgroundColor=backgroundColor,name=a)
 def get(self,name):
  if not name.endswith(".cplx"):
   name+=".cplx"
  return self.data[name]
 def getNames(self):
  return list(self.data.keys())


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
 def __init__(self,graphicsInstance,fileName,backgroundColor=(-1,-1,-1),folder=""):
  if folder!="":
   if not folder.endswith("/") and not folder.endswith("\\"):
    folder+="\\"
  from PIL import Image as image
  im=image.open(folder+fileName)
  rgb_im =im.convert("RGB")
  self.size=graphicsInstance.tileWidth
  self.pixdata=[]
  import copy
  dy=im.size[1]/self.size
  dx=im.size[0]/self.size
  y=0
  while y<im.size[1]:
   temp=[]
   x=0
   while x<im.size[0]:
    temp.append(rgb_im.getpixel((int(x),int(y))))
    x+=dx
   y+=dy
   self.pixdata.append(copy.copy(temp))
  self.backColor=backgroundColor
 def setBackgroundColor(self,color):
  self.backColor=color

class complexSprite:
 def __init__(self,graphicsInstance,folder,backgroundColor=(-1,-1,-1),name=""):
  if not folder.endswith("/") and not folder.endswith("\\"):
   folder+="\\"
  self.sprites=[]
  import os
  l=os.listdir(folder)
  text="__error__"
  for a in l:
   if a.endswith(".cplx"):
    if name=="" or a==name or a==name+".cplx":
     text=open(folder+a,"r").read()
  l=text.split("\n")
  self.positions=[]
  for a in l:
   temp=a.split(" ")
   self.sprites.append(sprite(graphicsInstance,temp[0],backgroundColor=backgroundColor,folder=folder))
   self.positions.append((int(temp[1]),int(temp[2])))


class textBox:
 def __init__(self,graphicsInstance,x,y,width,height,font="arialms",nRows=5,textColor=(255,255,255),backgroundColor=(0,0,0),border=False,bold=False,rowBoxes=False):
  self.nRows=nRows
  self.bold=bold
  tw=graphicsInstance.tileWidth
  self.textRect=(tw*x,tw*y,width*tw,height*tw)
  self.border=border
  self.font=font
  self.textColor=textColor
  self.backgroundColor=backgroundColor
  self.x=x
  self.y=y
  self.width=width
  self.height=height
  self.rowBoxes=rowBoxes
 def setBorder(self,border):
  self.border=border
 def setBackgroundColor(self,color):
  self.backgroundColor=color
 def setTextColor(self,color):
  self.textColor=color
 def setNRows(self,number):
  self.nRows=number
 def setFont(self,font):
  self.font=font
 def setBold(self,bold):
  self.bold=bold


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
  pygame.font.init()
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
 def update(self,fullQuit=False):
  events=pygame.event.get()
  pygame.display.flip()
  for event in events:
   if event.type==pygame.QUIT:
    pygame.quit()
    if fullQuit:
     exit()
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
 def highlight(self,x,y,color,width=1,height=1,lineWidth=3):
  pygame.draw.rect(screen,color,(x*self.tileWidth,y*self.tileWidth,width*self.tileWidth,height*self.tileWidth),lineWidth)
 def putSprite(self,x,y,sprite):
  xpart=x-int(x)
  ypart=y-int(y)
  x=int(x)
  y=int(y)
  xpart*=self.tileWidth
  ypart*=self.tileWidth
  xpart=int(xpart)
  ypart=int(ypart)
  px=x*self.tileWidth
  py=y*self.tileWidth
  for y in range(self.tileWidth):
   for x in range(self.tileWidth):
    pix=sprite.pixdata[y][x]
    if pix!=sprite.backColor:
     screen.set_at((x+px+xpart,y+py+ypart),pix)
 def putTextArray(self,textBox,textArray):
  if len(textArray)>textBox.nRows:
   raise(IndexError("size of text array is too large for textBox object to handle"))
  pygame.draw.rect(screen,textBox.backgroundColor,(textBox.x*self.tileWidth,textBox.y*self.tileWidth,textBox.width*self.tileWidth,textBox.height*self.tileWidth))
  if textBox.border:
   pygame.draw.rect(screen,textBox.textColor,(textBox.x*self.tileWidth,textBox.y*self.tileWidth,textBox.width*self.tileWidth,textBox.height*self.tileWidth),1)
  textSize=(textBox.height*self.tileWidth)/textBox.nRows
  font=pygame.font.SysFont(textBox.font,int(textSize),bold=textBox.bold)
  y=textBox.y
  for a in textArray:
   if textBox.rowBoxes:
    pygame.draw.rect(screen,textBox.textColor,(textBox.x*self.tileWidth,int(y),textBox.width*self.tileWidth,textSize),1)
   t=font.render(a,1,textBox.textColor)
   tpos=t.get_rect()
   tpos[0]=textBox.x
   tpos[1]=int(y)
   screen.blit(t,tpos)
   y+=textSize
 def putTextBox(self,textBox,text):
  if textBox.border:
   pygame.draw.rect(screen,textBox.textColor,(textBox.x*self.tileWidth,textBox.y*self.tileWidth,textBox.width*self.tileWidth,textBox.height*self.tileWidth))
  textSize=(textBox.height*self.tileWidth)/textBox.nRows
  font=pygame.font.SysFont(textBox.font,int(textSize),bold=textBox.bold)
  width=textBox.textRect[2]
  nextLine=""
  textArray=[]
  while len(text)>=1:
   rect=font.render(text,1,textBox.textColor).get_rect()
   if rect[2]>width:
    nextLine=text[len(text)-1]+nextLine
    text=text[0:len(text)-1]
   else:
    textArray.append(text)
    text=nextLine
    nextLine=""
  pygame.draw.rect(screen,textBox.backgroundColor,textBox.textRect)
  y=textBox.textRect[1]
  x=textBox.textRect[0]
  for text in textArray:
   t=font.render(text,1,textBox.textColor)
   tpos=t.get_rect()
   if textBox.rowBoxes:
    pygame.draw.rect(screen,textBox.textColor,(textBox.x*self.tileWidth,y,textBox.width*self.tileWidth,tpos[3]),1)
   tpos[0]=x
   tpos[1]=y
   screen.blit(t,tpos)
   y+=tpos[3]
 def putComplexSprite(self,x,y,complexSprite):
  for parse in enumerate(complexSprite.sprites):
   nx=complexSprite.positions[parse[0]][0]+x
   ny=complexSprite.positions[parse[0]][1]+y
   self.putSprite(nx,ny,parse[1])
 def removeSprite(self,x,y):
  xpart=x-int(x)
  ypart=y-int(y)
  xrange=[0,1]
  if xpart!=0:
   xrange=[0,2]
  yrange=[0,1]
  if ypart!=0:
   yrange=[0,2]
  x=int(x)
  y=int(y)
  for tx in range(xrange[0],xrange[1]):
   for ty in range(yrange[0],yrange[1]):
    pygame.draw.rect(screen,self.palette.get(self.matrix[y+ty][x+tx]),((x+tx)*self.tileWidth,(y+ty)*self.tileWidth,self.tileWidth,self.tileWidth))
 def removeComplexSprite(self,x,y,complexSprite):
  for parse in enumerate(complexSprite.sprites):
   nx=complexSprite.positions[parse[0]][0]+x
   ny=complexSprite.positions[parse[0]][1]+y
   self.removeSprite(nx,ny)
