keycodes={'BACKSPACE':8,'TAB':9,'CLEAR':12,'RETURN':13,'PAUSE':19,'ESCAPE':27,'SPACE':32,'EXCLAIM':33,'QUOTEDBL':34,'HASH':35,'DOLLAR':36,'AMPERSAND':38,'QUOTE':39,'LEFTPAREN':40,'RIGHTPAREN':41,'ASTERISK':42,'PLUS':43,'COMMA':44,'MINUS':45,'PERIOD':46,'SLASH':47,'0':48,'1':49,'2':50,'3':51,'4':52,'5':53,'6':54,'7':55,'8':56,'9':57,'COLON':58,'SEMICOLON':59,'LESS':60,'EQUALS':61,'GREATER':62,'QUESTION':63,'AT':64,'LEFTBRACKET':91,'BACKSLASH':92,'RIGHTBRACKET':93,'CARET':94,'UNDERSCORE':95,'BACKQUOTE':96,'a':97,'b':98,'c':99,'d':100,'e':101,'f':102,'g':103,'h':104,'i':105,'j':106,'k':107,'l':108,'m':109,'n':110,'o':111,'p':112,'q':113,'r':114,'s':115,'t':116,'u':117,'v':118,'w':119,'x':120,'y':121,'z':122,'DELETE':127,'KP0':256,'KP1':257,'KP2':258,'KP3':259,'KP4':260,'KP5':261,'KP6':262,'KP7':263,'KP8':264,'KP9':265,'KP_PERIOD':266,'KP_DIVIDE':267,'KP_MULTIPLY':268,'KP_MINUS':269,'KP_PLUS':270,'KP_ENTER':271,'KP_EQUALS':272,'UP':273,'DOWN':274,'RIGHT':275,'LEFT':276,'INSERT':277,'HOME':278,'END':279,'PAGEUP':280,'PAGEDOWN':281,'F1':282,'F2':283,'F3':284,'F4':285,'F5':286,'F6':287,'F7':288,'F8':289,'F9':290,'F10':291,'F11':292,'F12':293,'F13':294,'F14':295,'F15':296,'NUMLOCK':300,'CAPSLOCK':301,'SCROLLOCK':302,'RSHIFT':303,'LSHIFT':304,'RCTRL':305,'LCTRL':306,'RALT':307,'LALT':308,'RMETA':309,'LMETA':310,'LSUPER':311,'RSUPER':312,'MODE':313,'HELP':315,'PRINT':316,'SYSREQ':317,'BREAK':318,'MENU':319,'POWER':320,'EURO':321}

from PIL import Image as image
import time

class sizeSprite:
	def __init__(self,graphicsInstance,fileName,width,height,backgroundColor=(-1,-1,-1),folder=""):
		if folder!="":
			if not folder.endswith("/") and not folder.endswith("\\"):
				folder+="\\"
		self.source=folder+fileName
		self.width=width
		self.size=graphicsInstance.tileWidth
		self.height=height
		self.trackerNum=graphicsInstance.spriteReloadNum
		self.backColor=backgroundColor
		self.pixdata=[]
		width=int(width*self.size)
		height=int(height*self.size)
		im=image.open(self.source).resize((width,height)).convert("RGB")
		for y in range(height):
			buffer=[]
			colorBuffer=[]
			blanks=0
			for x in range(width):
				color=im.getpixel((x,y))[:3][::-1]
				if color!=self.backColor:
					if blanks>0:
						buffer.append(blanks)
						blanks=0
					colorBuffer+=[a for a in color]+[0]
				else:
					if len(colorBuffer)>0:
						buffer.append(colorBuffer.copy())
						colorBuffer=[]
					blanks+=1
			if len(colorBuffer)>0:
				buffer.append(colorBuffer.copy())
				colorBuffer=[]
			self.pixdata.append(buffer.copy())
	def setBackgroundColor(self,backgroundColor):
		self.backColor=backgroundColor
		self.reload()
	def reload(self,graphicsInstance=None):
		if graphicsInstance!=None:
			self.trackerNum=graphicsInstance.spriteReloadNum
			self.size=graphicsInstance.tileWidth
		self.pixdata=[]
		width=int(self.width*self.size)
		height=int(self.height*self.size)
		im=image.open(self.source).resize((width,height)).convert("RGB")
		for y in range(height):
			buffer=[]
			colorBuffer=[]
			blanks=0
			for x in range(width):
				color=im.getpixel((x,y))[:3][::-1]
				if color!=self.backColor:
					if blanks>0:
						buffer.append(blanks)
						blanks=0
					colorBuffer+=[a for a in color]+[0]
				else:
					if len(colorBuffer)>0:
						buffer.append(colorBuffer.copy())
						colorBuffer=[]
					blanks+=1
			if len(colorBuffer)>0:
				buffer.append(colorBuffer.copy())
				colorBuffer=[]
			self.pixdata.append(buffer.copy())

class spriteManager:
	def __init__(self,graphicsInstance,*spriteFolder,backgroundColor=(-1,-1,-1)):
		if len(spriteFolder)==0:
			folder=""
		else:
			folder=spriteFolder[0]
		import os
		self.data={}
		lst=os.listdir(folder if folder!="" else None)
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
		if type(index)==str:
			return tuple(int(index[i:i+2], 16) for i in (0, 2, 4))#thanks to John1024 for this beautiful line of code
		if type(index)==tuple:
			return index
		return self.colors[index]
	def add(self,color):
		self.colors.append(color)

class legacySprite:
	def __init__(self,graphicsInstance,fileName,backgroundColor=(-1,-1,-1),folder=""):
		if folder!="":
			if not folder.endswith("/") and not folder.endswith("\\"):
				folder+="\\"
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

class sprite:
	def __init__(self,graphicsInstance,fileName,backgroundColor=(-1,-1,-1),folder=""):
		if folder!="":
			if not folder.endswith("/") and not folder.endswith("\\"):
				folder+="\\"
		self.source=folder+fileName
		im=image.open(folder+fileName)
		rgb_im =im.convert("RGB")
		self.size=graphicsInstance.tileWidth
		self.trackerNum=graphicsInstance.spriteReloadNum#used for manual and automatic sprite reloading
		self.pixdata=[]
		rgb_im=im.resize((self.size,self.size))
		self.backColor=backgroundColor
		for y in range(self.size):
			buffer=[]
			colorBuffer=[]
			blanks=0
			for x in range(self.size):
				color=rgb_im.getpixel((x,y))[:3][::-1]
				if color!=self.backColor:
					if blanks>0:
						buffer.append(blanks)
						blanks=0
					colorBuffer+=[a for a in color]+[0]
				else:
					if len(colorBuffer)>0:
						buffer.append(colorBuffer.copy())
						colorBuffer=[]
					blanks+=1
			if len(colorBuffer)>0:
				buffer.append(colorBuffer.copy())
				colorBuffer=[]
			self.pixdata.append(buffer.copy())
	def setBackgroundColor(self,color):
		self.backColor=color
		self.reload()
	def reload(self,graphicsInstance=None):
		if graphicsInstance!=None:
			self.size=graphicsInstance.tileWidth
			self.trackerNum=graphicsInstance.spriteReloadNum
		im=image.open(self.source)
		rgb_im =im.convert("RGB")
		self.pixdata=[]
		rgb_im=im.resize((self.size,self.size))
		for y in range(self.size):
			buffer=[]
			colorBuffer=[]
			blanks=0
			for x in range(self.size):
				color=rgb_im.getpixel((x,y))[:3][::-1]
				if color!=self.backColor:
					if blanks>0:
						buffer.append(blanks)
						blanks=0
					colorBuffer+=[a for a in color]+[0]
				else:
					if len(colorBuffer)>0:
						buffer.append(colorBuffer.copy())
						colorBuffer=[]
					blanks+=1
			if len(colorBuffer)>0:
				buffer.append(colorBuffer.copy())
				colorBuffer=[]
			self.pixdata.append(buffer.copy())

class legacyComplexSprite:
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
			self.sprites.append(legacySprite(graphicsInstance,temp[0],backgroundColor=backgroundColor,folder=folder))
			self.positions.append((int(temp[1]),int(temp[2])))


class complexSprite:
	def __init__(self,graphicsInstance,folder,backgroundColor=(-1,-1,-1),name=""):
		self.size=graphicsInstance.tileWidth
		self.backColor=backgroundColor
		self.trackerNum=graphicsInstance.spriteReloadNum
		if not folder.endswith("/") and not folder.endswith("\\"):
			folder+="\\"
		import os
		self.folder=folder
		l=os.listdir(folder)
		text="__error__"
		for a in l:
			if a.endswith(".cplx"):
				if name=="" or a==name or a==name+".cplx":
					text=open(folder+a,"r").read()
					self.source=folder+a
		l=text.split("\n")
		sxp=[]
		syp=[]
		snames=[]
		for a in l:
			temp=a.split(" ")
			snames.append(temp[0])
			sxp.append(int(temp[1]))
			syp.append(int(temp[2]))
		self.height=max(syp)+1
		self.width=max(sxp)+1
		mat=[]
		for y in range(self.height):
			mat.append(([None]*self.width).copy())
		for x, y, snames in zip(sxp,syp,snames):
			mat[y][x]=image.open(self.folder+snames).resize((self.size,self.size)).convert("RGB")
		self.pixdata=[]
		for tileY in range(self.height):
			for pixY in range(self.size):
				buffer=[]
				colorBuffer=[]
				blanks=0
				for tileX in range(self.width):
					if mat[tileY][tileX]!=None:
						for pixX in range(self.size):
							color=mat[tileY][tileX].getpixel((pixX,pixY))[:3][::-1]
							if color!=self.backColor:
								if blanks>0:
									buffer.append(blanks)
									blanks=0
								colorBuffer+=[a for a in color]+[0]
							else:
								if len(colorBuffer)>0:
									buffer.append(colorBuffer.copy())
									colorBuffer=[]
								blanks+=1
					else:
						if len(colorBuffer)>0:
							buffer.append(colorBuffer.copy())
							colorBuffer=[]
						blanks+=self.size
				if len(colorBuffer)>0:
					buffer.append(colorBuffer.copy())
				self.pixdata.append(buffer.copy())
	def setBackgroundColor(self,backgroundColor):
		self.backColor=backgroundColor
		self.reload()
	def reload(self,graphicsInstance=None):
		if graphicsInstance!=None:
			self.size=graphicsInstance.tileWidth
			self.trackerNum=graphicsInstance.spriteReloadNum
		text=open(self.source,"r").read()
		l=text.split("\n")
		sxp=[]
		syp=[]
		snames=[]
		for a in l:
			temp=a.split(" ")
			snames.append(temp[0])
			sxp.append(int(temp[1]))
			syp.append(int(temp[2]))
		self.height=max(syp)+1
		self.width=max(sxp)+1
		mat=[]
		for y in range(self.height):
			mat.append(([None]*self.width).copy())
		for x, y, snames in zip(sxp,syp,snames):
			mat[y][x]=image.open(self.folder+snames).resize((self.size,self.size)).convert("RGB")
		self.pixdata=[]
		for tileY in range(self.height):
			for pixY in range(self.size):
				buffer=[]
				colorBuffer=[]
				blanks=0
				for tileX in range(self.width):
					if mat[tileY][tileX]!=None:
						for pixX in range(self.size):
							color=mat[tileY][tileX].getpixel((pixX,pixY))[:3][::-1]
							if color!=self.backColor:
								if blanks>0:
									buffer.append(blanks)
									blanks=0
								colorBuffer+=[a for a in color]+[0]
							else:
								if len(colorBuffer)>0:
									buffer.append(colorBuffer.copy())
									colorBuffer=[]
								blanks+=1
					else:
						if len(colorBuffer)>0:
							buffer.append(colorBuffer.copy())
							colorBuffer=[]
						blanks+=self.size
				if len(colorBuffer)>0:
					buffer.append(colorBuffer.copy())
				self.pixdata.append(buffer.copy())


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
	def __init__(self,width,height,palette="standard",roughSize=-1,screenWidth=None,screenHeight=None,fullScreen=False,roughPercent=-1,fullScreenKey=292,noResize=False,fps=-1):
		self.fsKey=fullScreenKey
		global pygame,screen
		import pygame
		self.noResize=noResize
		pygame.init()
		obj=pygame.display.Info()
		if screenWidth==None:
			screenWidth=obj.current_w
		if screenHeight==None:
			screenHeight=obj.current_h
		self.fullScreenWidth=obj.current_w
		self.fullScreenHeight=obj.current_h
		if roughSize!=-1:
			screenWidth=roughSize
			screenHeight=roughSize
		elif roughPercent!=-1:
			screenWidth=roughPercent*screenWidth
			screenHeight=roughPercent*screenHeight
		if palette=="standard":
			palette=colorPalette((0,0,0),(0,0,255),(0,255,0),(0,255,255),(255,0,0),(255,0,255),(255,255,0),(255,255,255))
		temp1=int(screenWidth/width)
		temp2=int(screenHeight/height)
		self.tileWidth=temp1
		if temp2<temp1:
			self.tileWidth=temp2
		self.width=width
		self.height=height
		self.screenWidth=self.tileWidth*width
		self.screenHeight=self.tileWidth*height
		self.size=(self.screenWidth,self.screenHeight)
		pygame.font.init()
		if not fullScreen:
			if self.noResize:
				screen=pygame.display.set_mode(self.size)
			else:
				screen=pygame.display.set_mode(self.size,pygame.RESIZABLE)
		else:
			screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
			self.size=screen.get_size()
			self.screenWidth=self.size[0]
			self.screenHeight=self.size[1]
		screen.fill(palette.get(0))
		self.matrix=[]
		self.palette=palette
		self.fullScreen=fullScreen
		self.fullscreenToggle=False
		import copy
		temp=[]
		for x in range(width):
			temp.append(0)
		for y in range(height):
			self.matrix.append(copy.copy(temp))
		self.drawCall=True
		self.spriteReloadNum=0
		self.fullScreenOutRes=self.size
		self.resizeBool=False
		self.fullScreenKey=fullScreenKey
		self.targetDelta=1/fps
		self.deltaTime=0
		self.frametime=time.time()
	def setIcon(self,imageName):
		if not "." in imageName:
			imageName+=".png"
		surf=pygame.image.load(imageName)
		pygame.display.set_icon(surf)
	def update(self,fullQuit=False):
		t=time.time()
		self.deltatime=t-self.frametime
		self.frametime=t
		if self.deltaTime<self.targetDelta:
			offset=self.targetDelta-self.deltaTime
			time.sleep(offset)
			self.deltaTime+=offset
		if self.drawCall:
			pygame.display.flip()
			self.drawCall=False
		events=pygame.event.get()
		for event in events:
			if event.type==pygame.QUIT:
				pygame.quit()
				if fullQuit:
					exit()
			if event.type==pygame.KEYDOWN and event.key==self.fullScreenKey:
				self.fullscreenToggle=True
			if not self.noResize and (event.type==pygame.VIDEORESIZE or self.fullscreenToggle or self.resizeBool):
				self.resized=True
				global screen
				if self.fullScreen:
					oldwidthoffset=self.fullScreenWidth-self.width*self.tileWidth
					oldheightoffset=self.fullScreenHeight-self.height*self.tileWidth
				else:
					oldwidthoffset=None
					oldheightoffset=None
				if self.fullscreenToggle:
					self.fullScreen=not self.fullScreen
					if self.fullScreen:
						width=self.fullScreenWidth
						height=self.fullScreenHeight
					else:
						width, height=self.fullScreenOutRes
				elif self.resizeBool:
					width, height=self.size
				else:
					width, height=(event.w,event.h)
				self.fullscreenToggle=False
				oldwidth=self.tileWidth
				temp1=int(width/self.width)
				temp2=int(height/self.height)
				self.tileWidth=min(temp1,temp2)
				self.screenWidth=self.tileWidth*self.width
				self.screenHeight=self.tileWidth*self.height
				self.size=(self.screenWidth,self.screenHeight)
				if oldwidthoffset==None:
					screenBackup=pygame.transform.scale(screen,(self.screenWidth,self.screenHeight))
				else:
					screenBackup=pygame.Surface((self.fullScreenWidth-oldwidthoffset,self.fullScreenHeight-oldheightoffset))
					screenBackup.blit(screen,(0,0),(0,0,self.fullScreenWidth-oldwidthoffset,self.fullScreenHeight-oldheightoffset))
					screenBackup=pygame.transform.scale(screenBackup,(self.screenWidth,self.screenWidth))
				if not self.fullScreen:
					self.fullScreenOutRes=self.size
					screen=pygame.display.set_mode(self.size,pygame.RESIZABLE)
				else:
					screen=pygame.display.set_mode((self.fullScreenWidth,self.fullScreenHeight),pygame.FULLSCREEN)
				if not self.resizeBool:
					screen.blit(screenBackup,(0,0))
					tempsize=screen.get_size()
					b1=tempsize[0]>self.screenWidth
					b2=tempsize[1]>self.screenHeight
					if b1:
						pygame.draw.rect(screen,self.palette.get(0),(self.screenWidth,0,tempsize[0]-self.screenWidth,self.screenHeight))
					if b2:
						pygame.draw.rect(screen,self.palette.get(0),(0,self.screenHeight,self.screenWidth,tempsize[1]-self.screenHeight))
					if b1 and b2:
						pygame.draw.rect(screen,self.palette.get(0),(self.screenWidth,self.screenHeight,tempsize[0]-self.screenWidth,tempsize[1]-self.screenHeight))
				else:
					screen.fill((0,0,0))
					self.resizeBool=False
				pygame.display.flip()
				pygame.event.get()
				if oldwidth!=self.tileWidth:
					self.spriteReloadNum+=1
	def setResizeable(self,resizeable):
		global screen
		if resizeable==self.noResize:
			self.noResize=not resizeable
			tempscreen=pygame.Surface((self.screenWidth,self.screenHeight))
			tempscreen.blit(screen,(0,0))
			if self.noResize:
				screen=pygame.display.set_mode((self.screenWidth,self.screenHeight))
			else:
				screen=pygame.display.set_mode((self.screenWidth,self.screenHeight),pygame.RESIZABLE)
			screen.blit(tempscreen,(0,0))
	def getResizedBool(self):
		out=self.resized
		self.resized=False
		return out
	def setFPS(self,fps):
		self.targetDelta=1/fps
	def resize(self,width,height):
		self.width=width
		self.height=height
		self.resizeBool=True
		self.matrix=[]
		for y in range(height):
			self.matrix.append(([0]*self.width).copy())
		self.update()
	def resizeScreen(self,pixelWidth,pixelHeight):
		self.size=(pixelWidth,pixelHeight)
		self.resizeBool=True
		self.update()
	def screenshot(self,imageName):
		pygame.image.save(screen,imageName)
	def pixelPut(self,x,y,colorIndex):
		self.drawCall=True
		screen.set_at((x,y),self.palette.get(colorIndex))
	def translate(self,x,y,deltaX,deltaY,width=1,height=1):
		self.drawCall=True
		self.pixelTranslate((x*self.tileWidth,y*self.tileWidth,width*self.tileWidth,height*self.tileWidth),deltaX*self.tileWidth,deltaY*self.tileWidth)
	def pixelTranslate(self,rect,deltaX,deltaY):
		self.drawCall=True
		tempSurface=screen.subsurface(rect)
		finalSurface=pygame.Surface((rect[2],rect[3]))
		finalSurface.blit(tempSurface,(0,0))
		screen.blit(finalSurface,(rect[0]+deltaX,rect[1]+deltaY))
	def pixelRect(self,rect,colorIndex,lineWidth=None):
		self.drawCall=True
		if lineWidth==None:
			pygame.draw.rect(screen,self.palette.get(colorIndex),rect)
		else:
			pygame.draw.rect(screen,self.palette.get(colorIndex),rect,lineWidth)
	def pixelLine(self,c1,c2,colorIndex,width=1):
		self.drawCall=True
		pygame.draw.line(screen,self.palette.get(colorIndex),c1,c2,width)
	def line(self,c1,c2,colorIndex,width=1):
		self.drawCall=True
		pygame.draw.line(screen,self.palette.get(colorIndex),(c1[0]*self.tileWidth+int(self.tileWidth/2),c1[1]*self.tileWidth+int(self.tileWidth/2)),(c2[0]*self.tileWidth+int(self.tileWidth/2),c2[1]*self.tileWidth+int(self.tileWidth/2)),width)
	def put(self,x,y,colorIndex,width=1,height=1):
		self.drawCall=True
		for a in range(width):
			for b in range(height):
				self.matrix[y+b][x+a]=colorIndex
				pygame.draw.rect(screen,self.palette.get(colorIndex),((x+a)*self.tileWidth,(y+b)*self.tileWidth,self.tileWidth,self.tileWidth))
	def get(self,x,y):
		return self.matrix[y][x]
	def redraw(self):
		self.drawCall=True
		for a in range(self.width):
			for b in range(self.height):
				pygame.draw.rect(screen,self.palette.get(self.matrix[b][a]),((a)*self.tileWidth,(b)*self.tileWidth,self.tileWidth,self.tileWidth))
	def setName(self,name):
		self.drawCall=True
		pygame.display.set_caption(name)
	def fill(self,colorIndex):
		self.drawCall=True
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
	def outline(self,color,x=0,y=0,width=-1,height=-1):
		self.drawCall=True
		color=self.palette.get(color)
		if width==-1:
			width=self.screenWidth
		else:
			width=width*self.tileWidth
		if height==-1:
			height=self.screenHeight
		else:
			height=height*self.tileWidth
		fx=x*self.tileWidth
		fy=y*self.tileWidth
		for x in range(fx,width+1,self.tileWidth):
			pygame.draw.line(screen,color,(x,0),(x,height))
		for y in range(fy,height+1,self.tileWidth):
			pygame.draw.line(screen,color,(0,y),(width,y))
	def checkKey(self,key):
		if key==self.fsKey:
			print("TILEGRAPHICS WARNING, the key being checked is internally bound to fullscreen toggle\nIf you want to use this key, change the fullscreen key with the fullScreenKey=<key> when initializing graphics instance")
		return pygame.key.get_pressed()[key]==1
	def checkClick(self,button=0):
		return pygame.mouse.get_pressed()[button]==1
	def quit(self):
		pygame.quit()
	def highlight(self,x,y,color,width=1,height=1,lineWidth=3):
		self.drawCall=True
		pygame.draw.rect(screen,self.palette.get(color),(x*self.tileWidth,y*self.tileWidth,width*self.tileWidth,height*self.tileWidth),lineWidth)
	def reloadSprites(self):
		self.spriteReloadNum+=1
	def putLegacySprite(self,x,y,sprite):
		self.drawCall=True
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
	def putSprite(self,x,y,sprite):
		if sprite.trackerNum!=self.spriteReloadNum:
			sprite.reload(graphicsInstance=self)
		self.drawCall=True
		x*=self.tileWidth
		y*=self.tileWidth
		buffer=screen.get_buffer()
#		ntArray=list(buffer.raw)
		for yOff, line in enumerate(sprite.pixdata):
			xOff=0
			for item in line:
				 if type(item)==int:
					 xOff+=item
				 else:
					 startIndex=(yOff+y)*self.screenWidth*4+(xOff+x)*4
					 buffer.write(bytes(item),offset=startIndex)
#					 ntArray[startIndex:startIndex+len(item)]=item
					 xOff+=int(len(item)/4)
#		buffer.write(bytes(ntArray))
		del buffer
	def putComplexSprite(self,x,y,complexSprite):
		self.putSprite(x,y,complexSprite)
	def putSizeSprite(self,x,y,sizeSprite):
		self.putSprite(x,y,sizeSprite)
	def putTextArray(self,textBox,textArray):
		self.drawCall=True
		if len(textArray)>textBox.nRows:
			raise(IndexError("size of text array is too large for textBox object to handle"))
		pygame.draw.rect(screen,textBox.backgroundColor,(textBox.x*self.tileWidth,textBox.y*self.tileWidth,textBox.width*self.tileWidth,textBox.height*self.tileWidth))
		if textBox.border:
			pygame.draw.rect(screen,textBox.textColor,(textBox.x*self.tileWidth,textBox.y*self.tileWidth,textBox.width*self.tileWidth,textBox.height*self.tileWidth),1)
		textSize=(textBox.height*self.tileWidth)/textBox.nRows
		font=pygame.font.SysFont(textBox.font,int(textSize),bold=textBox.bold)
		y=textBox.y*self.tileWidth
		for a in textArray:
			if textBox.rowBoxes:
				pygame.draw.rect(screen,textBox.textColor,(textBox.x*self.tileWidth,int(y),textBox.width*self.tileWidth,textSize),1)
			t=font.render(a,1,textBox.textColor)
			tpos=t.get_rect()
			tpos[0]=textBox.x*self.tileWidth
			tpos[1]=int(y)
			screen.blit(t,tpos)
			y+=textSize
	def putTextBox(self,textBox,text):
		self.drawCall=True
		pygame.draw.rect(screen,textBox.backgroundColor,(textBox.x*self.tileWidth,textBox.y*self.tileWidth,textBox.width*self.tileWidth,textBox.height*self.tileWidth))
		if textBox.border:
			pygame.draw.rect(screen,textBox.textColor,(textBox.x*self.tileWidth,textBox.y*self.tileWidth,textBox.width*self.tileWidth,textBox.height*self.tileWidth),1)
		textSize=textBox.height*self.tileWidth
		font=pygame.font.SysFont(textBox.font,int(textSize),bold=textBox.bold)
		y=textBox.y*self.tileWidth
		t=font.render(textBox,1,textBox.textColor)
		tpos=t.get_rect()
		tpos[0]=textBox.x*self.tileWidth
		tpos[1]=int(y)
		screen.blit(t,tpos)
		y+=textSize
	def putLegacyComplexSprite(self,x,y,complexSprite):
		self.drawCall=True
		for parse in enumerate(complexSprite.sprites):
			nx=complexSprite.positions[parse[0]][0]+x
			ny=complexSprite.positions[parse[0]][1]+y
			self.putLegacySprite(nx,ny,parse[1])
	def putSecLegacyComplexSprite(self,x,y,complexSprite,spritex,spritey):
		self.drawCall=True
		for parse in enumerate(complexSprite.sprites):
			nx=complexSprite.positions[parse[0]][0]
			ny=complexSprite.positions[parse[0]][1]
			if nx==spritex and ny==spritey:
				self.putLegacySprite(nx+x,ny+y,parse[1])
	def removeSprite(self,x,y):
		self.drawCall=True
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
		self.drawCall=True
		for parse in enumerate(complexSprite.sprites):
			nx=complexSprite.positions[parse[0]][0]+x
			ny=complexSprite.positions[parse[0]][1]+y
			self.removeSprite(nx,ny)
