#Catacomb Johnson
#WORKING WARPS
#Nathan Christie
#11/19/2019

'''
PLEASE MAPS ALL LOAD AT ONCE
STORE IN A VARIABLE AND CHANGE CURRENT MAP

'''
from tkinter import *
import PIL.Image, PIL.ImageTk
import random
import os.path
import winsound as snd
import time

class Player(object):
    def __init__(self, hungerLev, hungerMes, pDirection, orbsCollected, pLocation, level=1):
        self.health=hungerLev
        self.mes=hungerMes
        self.direction=pDirection
        self.orbs=orbsCollected
        self.location=pLocation
        self.myAir="empty"
        self.myFire=[]
        self.moveEna=True
        self.AIR_COOLDOWN=10
        self.FIRE_COOLDOWN=30
        self.COOLDOWN_TRIG=False
        self.DMG_COOLDOWN=20
        self.MOV_COOLDOWN=3
        self.airActCool=self.AIR_COOLDOWN
        self.movActCool=self.MOV_COOLDOWN
        self.activeCooldown=self.FIRE_COOLDOWN
        self.dmgActCool=self.DMG_COOLDOWN
        
    def moveFor(self,event=0): #moves player forwards
        if self.moveEna==True:
            if self.movActCool==self.MOV_COOLDOWN:
                self.movActCool=0
                if self.direction==1:
                    #print "north"
                    if (self.location[0],self.location[1]-1) in currentMap.wallSet: #Statements like this check if the player is going into a wall
                        #actLog.append("*thud*")
                        LogUpdater.messages.append("*thud*")
                    else:
                        self.location=(self.location[0],self.location[1]-1)
                        self.health+=-1
                elif self.direction==2:
                    #print "east"
                    if (self.location[0]+1,self.location[1]) in currentMap.wallSet:
                        #actLog.append("*thud*")
                        LogUpdater.messages.append("*thud*")
                    else:
                        self.location=(self.location[0]+1,self.location[1])
                        self.health+=-1
        
                elif self.direction==3:
                    #print "south"
                    if (self.location[0],self.location[1]+1) in currentMap.wallSet:
                        #actLog.append("*thud*")
                        LogUpdater.messages.append("*thud*")
                    else:
                        self.location=(self.location[0],self.location[1]+1)
                        self.health+=-1
                elif self.direction==4:
                    #print "west"
                    if (self.location[0]-1,self.location[1]) in currentMap.wallSet:
                        #actLog.append("*thud*")
                        LogUpdater.messages.append("*thud*")
                    else:
                        self.location=(self.location[0]-1,self.location[1])
                        self.health+=-1
                #drawMap()
    
    def moveBak(self,event=0): #moves player backwards
        if self.moveEna==True:
            if self.movActCool==self.MOV_COOLDOWN:
                self.movActCool=0
                if self.direction==1:
                    #print "south"
                    if (self.location[0],self.location[1]+1) in currentMap.wallSet:
                        #actLog.append("*thud*")
                        LogUpdater.messages.append("*thud*")
                    else:
                        self.location=(self.location[0],self.location[1]+1)
                        self.health+=-1
                elif self.direction==2:
                    #print "west"
                    if (self.location[0]-1,self.location[1]) in currentMap.wallSet:
                        #actLog.append("*thud*")
                        LogUpdater.messages.append("*thud*")
                    else:
                        self.location=(self.location[0]-1,self.location[1])
                        self.health+=-1
                elif self.direction==3:
                    #print "north"
                    if (self.location[0],self.location[1]-1) in currentMap.wallSet:
                        #actLog.append("*thud*")
                        LogUpdater.messages.append("*thud*")
                    else:
                        self.location=(self.location[0],self.location[1]-1)
                        self.health+=-1
                elif self.direction==4:
                    #print "east"
                    if (self.location[0]+1,self.location[1]) in currentMap.wallSet:
                        #actLog.append("*thud*")
                        LogUpdater.messages.append("*thud*")
                    else:
                        self.location=(self.location[0]+1,self.location[1])
                        self.health+=-1
                #drawMap()
    
    def turnLeft(self,event=0): #turns the player left
        if self.moveEna==True:
            #print "left"
            if self.direction!=1:
                self.direction+=-1
            elif self.direction!=-1:
                self.direction=4
            #drawMap()
    
    def turnRight(self,event=0): #turns the player right
        if self.moveEna==True:
            #print "right"
            if self.direction!=4 and self.direction!=-1:
                self.direction+=1
            elif self.direction!=-1:
                self.direction=1
            #drawMap()
    
    def shootFire(self,event=0): #shoot Fire
        if self.moveEna==True:
            if self.health!="DEAD":
                if self.COOLDOWN_TRIG==False:
                    self.myFire.append(fireBall(self.location, self.direction))
                    #print  list(x.origin for x in self.myFire)
                    self.COOLDOWN_TRIG=True
                    
    def airBlast(self,event=0):
        if self.moveEna==True:
            if self.airActCool==self.AIR_COOLDOWN:
                self.myAir=airBlastObj(self.location, self.direction)
                self.airActCool=0
            
    def hurt(self, damage): #hurts the player
        if self.dmgActCool==self.DMG_COOLDOWN:
            text="[Johnson] took "+str(damage)+" damage!"
            LogUpdater.messages.append(text)
            self.health+=damage*-1
            self.dmgActCool=0
            if self.health<=0:
                self.die()
                
    def die(self):
        UserPlayer.direction=-1 #This makes the player invisible
        self.moveEna=False
        UserPlayer.health="DEAD"
        self.dmgActCool=self.DMG_COOLDOWN+1
        LogUpdater.messages.append("You have joined the ranks of the dead.")
        
    def toggleMov(self):
        if self.moveEna==True:
            self.moveEna=False
        else:
            self.moveEna=True
        
class fireBall(object):
    def __init__(self, origin, direction):
        self.origin=origin
        self.direction=direction
        self.imgs=[fireNSp,fireESp,fireSSp,fireWSp]
        self.img=self.imgs[direction-1]
        #self.add()
    def move(self): #moves fireball in direction fired
        
        if self.direction==1:
            if (self.origin[0],self.origin[1]-1) not in currentMap.wallSet:
                self.origin=(self.origin[0],self.origin[1]-1)
                #drawMap()
                #visScreen.after(100, self.move(direction))
            else:
                UserPlayer.myFire.remove(self)
                self.__del__()
        if self.direction==2:
            if (self.origin[0]+1,self.origin[1]) not in currentMap.wallSet:
                self.origin=(self.origin[0]+1,self.origin[1])
                #drawMap()
                #visScreen.after(100, self.move(direction))
            else:
                UserPlayer.myFire.remove(self)
                self.__del__()
        if self.direction==3:
            if (self.origin[0],self.origin[1]+1) not in currentMap.wallSet:
                self.origin=(self.origin[0],self.origin[1]+1)
                #drawMap()
                #visScreen.after(100, self.move(direction))
            else:
                UserPlayer.myFire.remove(self)
                self.__del__()
        if self.direction==4:
            if (self.origin[0]-1,self.origin[1]) not in currentMap.wallSet:
                self.origin=(self.origin[0]-1,self.origin[1])
                #drawMap()
                #visScreen.after(100, self.move(direction))
            else:
                UserPlayer.myFire.remove(self)
                self.__del__()
    def add(self):
        fireSet.append(self)
    def __del__(self):
        nothing()

class airBlastObj(object):
    def __init__(self, castLoc, castDir):
        imgAir=PIL.Image.open(os.path.join(directory, "asset/airBlast.png"))
        airSp=PIL.ImageTk.PhotoImage(imgAir)
        self.img=airSp
        if castDir==1:
            self.location1=(castLoc[0]-1,castLoc[1]-1)
            self.location2=(castLoc[0]+1,castLoc[1]-1)
        elif castDir==2:
            self.location1=(castLoc[0]+1,castLoc[1]-1)
            self.location2=(castLoc[0]+1,castLoc[1]+1)
        elif castDir==3:
            self.location1=(castLoc[0]-1,castLoc[1]+1)
            self.location2=(castLoc[0]+1,castLoc[1]+1)
        elif castDir==4:
            self.location1=(castLoc[0]-1,castLoc[1]-1)
            self.location2=(castLoc[0]-1,castLoc[1]+1)
        
#Utility Objects
class mapObj(object):
    def __init__(self, spawnerSet, wallSet, foodSet, orbSet, startLoc, warpSet, name, tileSet="dungeon"):
        self.wallSet=wallSet
        self.foodSet=foodSet
        self.orbSet=orbSet
        self.startLoc=startLoc
        self.tileSet=tileSet
        self.warpSet=warpSet
        self.warpDes=[]
        self.myName=name
        self.spawnerSet=spawnerSet
        self.dataLoc=os.path.join(directory, "maps/",name+".dat")
        self.dataFile= open(self.dataLoc, "r")
        self.dataLines=self.dataFile.readlines()
        self.dataFile.close()
        for lines in self.dataLines: #grabs the lines from the .dat and makes warp destinations
            coordStart=lines.find("(")+1
            xySplit=lines.find(",")
            coordEnd=lines.find(")")
            xVal,yVal=int(lines[coordStart:xySplit]),int(lines[xySplit+1:coordEnd])
            destination=(xVal,yVal)
            self.warpDes.append(destination)
  
class LogUpdater(object):
    def __init__(self):
      self.messages=[]
      self.processing=False
      self.LOG_COOLDOWN=2
      self.actCool=self.LOG_COOLDOWN
    def logUpdate(self):
        if len(self.messages)>0 and self.actCool==self.LOG_COOLDOWN:
            #self.processing==True
            global logObject
            logObject.insert(0,messageBox.create_text((5,210), fill="white", text=self.messages.pop(0), tags="text", font=("Fixedsys", 11), anchor=NW))
            self.scrollText()
    def scrollText(self,recursion=False, times=0):
        while times<5:
            messageBox.move("text",0,-5)
            times+=1
        else:
            self.actCool=0
            times=0
            #self.processing=False

#Classes for enemies
class enemy(object):
    def __init__(self,location):
        self.location=location
        self.atk=10 #default atk
        self.speed=5 #default Speed
        self.img=skelSp #default Img
        self.pattern=0
    def move(self,frame):
        if self.getDist()>5:
            if frame%self.speed==0:
                direction=random.randint(1,4)
                if direction==1:
                    if (self.location[0],self.location[1]-1) not in currentMap.wallSet:
                        self.location=(self.location[0],self.location[1]-1)
                if direction==2:
                    if (self.location[0]+1,self.location[1]) not in currentMap.wallSet:
                        self.location=(self.location[0]+1,self.location[1])
                if direction==3:
                    if (self.location[0],self.location[1]+1) not in currentMap.wallSet:
                        self.location=(self.location[0],self.location[1]+1)
                if direction==4:
                    if (self.location[0]-1,self.location[1]) not in currentMap.wallSet:
                        self.location=(self.location[0]-1,self.location[1])
        else:
            if frame%self.speed==0:
                if UserPlayer.location[1]<self.location[1]:#North
                    if (self.location[0],self.location[1]-1) not in currentMap.wallSet:
                        self.location=(self.location[0],self.location[1]-1)
                if UserPlayer.location[0]>self.location[0]:#East
                    if (self.location[0]+1,self.location[1]) not in currentMap.wallSet:
                        self.location=(self.location[0]+1,self.location[1])
                if UserPlayer.location[1]>self.location[1]: #South
                    if (self.location[0],self.location[1]+1) not in currentMap.wallSet:
                        self.location=(self.location[0],self.location[1]+1)
                if UserPlayer.location[0]<self.location[0]:#West
                    if (self.location[0]-1,self.location[1]) not in currentMap.wallSet:
                        self.location=(self.location[0]-1,self.location[1])
                
    def getDist(self):
        xDiff=abs(self.location[0]-UserPlayer.location[0])
        yDiff=abs(self.location[1]-UserPlayer.location[1])
        return xDiff+yDiff
        
class skeleton(enemy):
    def __init__(self, location):
        self.location=location
        self.atk=30
        self.speed=15
        self.img=skelSp
        self.pattern=(3,3,2,2,1,4,3)
        self.curPat=random.randint(0,6)
        
    def move(self,frame):
        if self.getDist()>5:
            if frame%self.speed==0:
                if self.pattern[self.curPat]==1:
                    if (self.location[0],self.location[1]-1) not in currentMap.wallSet:
                        self.location=(self.location[0],self.location[1]-1)
                if self.pattern[self.curPat]==2:
                    if (self.location[0]+1,self.location[1]) not in currentMap.wallSet:
                        self.location=(self.location[0]+1,self.location[1])
                if self.pattern[self.curPat]==3:
                    if (self.location[0],self.location[1]+1) not in currentMap.wallSet:
                        self.location=(self.location[0],self.location[1]+1)
                if self.pattern[self.curPat]==4:
                    if (self.location[0]-1,self.location[1]) not in currentMap.wallSet:
                        self.location=(self.location[0]-1,self.location[1])
                if self.curPat==6:
                    self.curPat=0
                else:
                    self.curPat+=1
        else:
            if frame%self.speed==0:
                randMod=random.randint(0,19)
                if randMod==19:
                    if (self.location[0]+1,self.location[1]) not in currentMap.wallSet:
                        self.location=(self.location[0]+1,self.location[1])
                elif randMod==18:
                    if (self.location[0]-1,self.location[1]) not in currentMap.wallSet:
                        self.location=(self.location[0]-1,self.location[1])
                else:
                    if UserPlayer.location[1]<self.location[1]:#North
                        if (self.location[0],self.location[1]-1) not in currentMap.wallSet:
                            self.location=(self.location[0],self.location[1]-1)
                    if UserPlayer.location[0]>self.location[0]:#East
                        if (self.location[0]+1,self.location[1]) not in currentMap.wallSet:
                            self.location=(self.location[0]+1,self.location[1])
                    if UserPlayer.location[1]>self.location[1]: #South
                        if (self.location[0],self.location[1]+1) not in currentMap.wallSet:
                            self.location=(self.location[0],self.location[1]+1)
                    if UserPlayer.location[0]<self.location[0]:#West
                        if (self.location[0]-1,self.location[1]) not in currentMap.wallSet:
                            self.location=(self.location[0]-1,self.location[1])
            
            
             
#functions
def update():
    global frameCounter
    checkDead()
    drawMap()
    LogUpdater.logUpdate()
    if frameCounter>0:
        frameCounter+=-1
    else:
        frameCounter=1000
        
    animate(frameCounter)
    
    if frameCounter%100==0: #triggers the spawn of enemies
       spawnEnemies()
       
    cooldown() 
    mapScreen.after(20, update)

def cooldown():
    if UserPlayer.movActCool!=UserPlayer.MOV_COOLDOWN:
        UserPlayer.movActCool+=1
        
    if UserPlayer.dmgActCool!=UserPlayer.DMG_COOLDOWN: #Cooldown for damage counter
        UserPlayer.dmgActCool+=1
        if UserPlayer.dmgActCool%4!=0 and UserPlayer.moveEna==True:
            messageBox.config(bg="red")
        else: 
            messageBox.config(bg="black")
    else:
        messageBox.config(bg="black")

    if UserPlayer.activeCooldown>0 and UserPlayer.COOLDOWN_TRIG==True: #cool down for player fireball
        UserPlayer.activeCooldown += -1
    else:
        UserPlayer.activeCooldown=UserPlayer.FIRE_COOLDOWN
        UserPlayer.COOLDOWN_TRIG=False
    if UserPlayer.airActCool!=UserPlayer.AIR_COOLDOWN:
        UserPlayer.airActCool+=1
        if UserPlayer.airActCool==5:
            UserPlayer.myAir="empty"
        
    if LogUpdater.actCool!=LogUpdater.LOG_COOLDOWN:
        LogUpdater.actCool+=1
        
def checkDead():
    if UserPlayer.health<=0:
        UserPlayer.die()
        
def spawnEnemies():   
    if len(eneSet)<50: #sets Limit of enemies
            if len(currentMap.spawnerSet)>0:
                eneSet.append(skeleton(random.choice(currentMap.spawnerSet)))#spawns skeleton at spawner
                    
def animate(frameCounter):
    global spawnSp
    if frameCounter%20==0:#animates spawners
        spawnSp=PIL.ImageTk.PhotoImage(imgSpawn1)
    elif frameCounter%20==10:
            spawnSp=PIL.ImageTk.PhotoImage(imgSpawn2)
    
def drawMap(): #updates the map each time the player turns or moves (also used to update evertime the user takes a movement action)
    listPos=0 #used to get order of tiles in mapcontent
    mapScreen.delete(ALL) #clears map so it can be redrawn
    tiles=[] #holds the images of walls and players placed on map
    fireLoc=[]
    eneLoc=[]
    
    #mapcontent contains the true map positions of the player and the walls around them
    mapcontent=[
            (UserPlayer.location[0]-5,UserPlayer.location[1]-5),(UserPlayer.location[0]-4,UserPlayer.location[1]-5),(UserPlayer.location[0]-3,UserPlayer.location[1]-5),(UserPlayer.location[0]-2,UserPlayer.location[1]-5),(UserPlayer.location[0]-1,UserPlayer.location[1]-5),(UserPlayer.location[0],UserPlayer.location[1]-5),(UserPlayer.location[0]+1,UserPlayer.location[1]-5),(UserPlayer.location[0]+2,UserPlayer.location[1]-5),(UserPlayer.location[0]+3,UserPlayer.location[1]-5),(UserPlayer.location[0]+4,UserPlayer.location[1]-5),(UserPlayer.location[0]+5,UserPlayer.location[1]-5),
            (UserPlayer.location[0]-5,UserPlayer.location[1]-4),(UserPlayer.location[0]-4,UserPlayer.location[1]-4),(UserPlayer.location[0]-3,UserPlayer.location[1]-4),(UserPlayer.location[0]-2,UserPlayer.location[1]-4),(UserPlayer.location[0]-1,UserPlayer.location[1]-4),(UserPlayer.location[0],UserPlayer.location[1]-4),(UserPlayer.location[0]+1,UserPlayer.location[1]-4),(UserPlayer.location[0]+2,UserPlayer.location[1]-4),(UserPlayer.location[0]+3,UserPlayer.location[1]-4),(UserPlayer.location[0]+4,UserPlayer.location[1]-4),(UserPlayer.location[0]+5,UserPlayer.location[1]-4),
            (UserPlayer.location[0]-5,UserPlayer.location[1]-3),(UserPlayer.location[0]-4,UserPlayer.location[1]-3),(UserPlayer.location[0]-3,UserPlayer.location[1]-3),(UserPlayer.location[0]-2,UserPlayer.location[1]-3),(UserPlayer.location[0]-1,UserPlayer.location[1]-3),(UserPlayer.location[0],UserPlayer.location[1]-3),(UserPlayer.location[0]+1,UserPlayer.location[1]-3),(UserPlayer.location[0]+2,UserPlayer.location[1]-3),(UserPlayer.location[0]+3,UserPlayer.location[1]-3),(UserPlayer.location[0]+4,UserPlayer.location[1]-3),(UserPlayer.location[0]+5,UserPlayer.location[1]-3),
            (UserPlayer.location[0]-5,UserPlayer.location[1]-2),(UserPlayer.location[0]-4,UserPlayer.location[1]-2),(UserPlayer.location[0]-3,UserPlayer.location[1]-2),(UserPlayer.location[0]-2,UserPlayer.location[1]-2),(UserPlayer.location[0]-1,UserPlayer.location[1]-2),(UserPlayer.location[0],UserPlayer.location[1]-2),(UserPlayer.location[0]+1,UserPlayer.location[1]-2),(UserPlayer.location[0]+2,UserPlayer.location[1]-2),(UserPlayer.location[0]+3,UserPlayer.location[1]-2),(UserPlayer.location[0]+4,UserPlayer.location[1]-2),(UserPlayer.location[0]+5,UserPlayer.location[1]-2),
            (UserPlayer.location[0]-5,UserPlayer.location[1]-1),(UserPlayer.location[0]-4,UserPlayer.location[1]-1),(UserPlayer.location[0]-3,UserPlayer.location[1]-1),(UserPlayer.location[0]-2,UserPlayer.location[1]-1),(UserPlayer.location[0]-1,UserPlayer.location[1]-1),(UserPlayer.location[0],UserPlayer.location[1]-1),(UserPlayer.location[0]+1,UserPlayer.location[1]-1),(UserPlayer.location[0]+2,UserPlayer.location[1]-1),(UserPlayer.location[0]+3,UserPlayer.location[1]-1),(UserPlayer.location[0]+4,UserPlayer.location[1]-1),(UserPlayer.location[0]+5,UserPlayer.location[1]-1),
            (UserPlayer.location[0]-5,UserPlayer.location[1]),(UserPlayer.location[0]-4,UserPlayer.location[1]),(UserPlayer.location[0]-3,UserPlayer.location[1]),(UserPlayer.location[0]-2,UserPlayer.location[1]),(UserPlayer.location[0]-1,UserPlayer.location[1]),UserPlayer.location,(UserPlayer.location[0]+1,UserPlayer.location[1]),(UserPlayer.location[0]+2,UserPlayer.location[1]),(UserPlayer.location[0]+3,UserPlayer.location[1]),(UserPlayer.location[0]+4,UserPlayer.location[1]),(UserPlayer.location[0]+5,UserPlayer.location[1]),
            (UserPlayer.location[0]-5,UserPlayer.location[1]+1),(UserPlayer.location[0]-4,UserPlayer.location[1]+1),(UserPlayer.location[0]-3,UserPlayer.location[1]+1),(UserPlayer.location[0]-2,UserPlayer.location[1]+1),(UserPlayer.location[0]-1,UserPlayer.location[1]+1),(UserPlayer.location[0],UserPlayer.location[1]+1),(UserPlayer.location[0]+1,UserPlayer.location[1]+1),(UserPlayer.location[0]+2,UserPlayer.location[1]+1),(UserPlayer.location[0]+3,UserPlayer.location[1]+1),(UserPlayer.location[0]+4,UserPlayer.location[1]+1),(UserPlayer.location[0]+5,UserPlayer.location[1]+1),
            (UserPlayer.location[0]-5,UserPlayer.location[1]+2),(UserPlayer.location[0]-4,UserPlayer.location[1]+2),(UserPlayer.location[0]-3,UserPlayer.location[1]+2),(UserPlayer.location[0]-2,UserPlayer.location[1]+2),(UserPlayer.location[0]-1,UserPlayer.location[1]+2),(UserPlayer.location[0],UserPlayer.location[1]+2),(UserPlayer.location[0]+1,UserPlayer.location[1]+2),(UserPlayer.location[0]+2,UserPlayer.location[1]+2),(UserPlayer.location[0]+3,UserPlayer.location[1]+2),(UserPlayer.location[0]+4,UserPlayer.location[1]+2),(UserPlayer.location[0]+5,UserPlayer.location[1]+2),
            (UserPlayer.location[0]-5,UserPlayer.location[1]+3),(UserPlayer.location[0]-4,UserPlayer.location[1]+3),(UserPlayer.location[0]-3,UserPlayer.location[1]+3),(UserPlayer.location[0]-2,UserPlayer.location[1]+3),(UserPlayer.location[0]-1,UserPlayer.location[1]+3),(UserPlayer.location[0],UserPlayer.location[1]+3),(UserPlayer.location[0]+1,UserPlayer.location[1]+3),(UserPlayer.location[0]+2,UserPlayer.location[1]+3),(UserPlayer.location[0]+3,UserPlayer.location[1]+3),(UserPlayer.location[0]+4,UserPlayer.location[1]+3),(UserPlayer.location[0]+5,UserPlayer.location[1]+3),
            (UserPlayer.location[0]-5,UserPlayer.location[1]+4),(UserPlayer.location[0]-4,UserPlayer.location[1]+4),(UserPlayer.location[0]-3,UserPlayer.location[1]+4),(UserPlayer.location[0]-2,UserPlayer.location[1]+4),(UserPlayer.location[0]-1,UserPlayer.location[1]+4),(UserPlayer.location[0],UserPlayer.location[1]+4),(UserPlayer.location[0]+1,UserPlayer.location[1]+4),(UserPlayer.location[0]+2,UserPlayer.location[1]+4),(UserPlayer.location[0]+3,UserPlayer.location[1]+4),(UserPlayer.location[0]+4,UserPlayer.location[1]+4),(UserPlayer.location[0]+5,UserPlayer.location[1]+4),
            (UserPlayer.location[0]-5,UserPlayer.location[1]+5),(UserPlayer.location[0]-4,UserPlayer.location[1]+5),(UserPlayer.location[0]-3,UserPlayer.location[1]+5),(UserPlayer.location[0]-2,UserPlayer.location[1]+5),(UserPlayer.location[0]-1,UserPlayer.location[1]+5),(UserPlayer.location[0],UserPlayer.location[1]+5),(UserPlayer.location[0]+1,UserPlayer.location[1]+5),(UserPlayer.location[0]+2,UserPlayer.location[1]+5),(UserPlayer.location[0]+3,UserPlayer.location[1]+5),(UserPlayer.location[0]+4,UserPlayer.location[1]+5),(UserPlayer.location[0]+5,UserPlayer.location[1]+5),
            ]
            
    if len(UserPlayer.myFire)!= 0:
        for fireball in UserPlayer.myFire: #moves each fireball (needed here so screen updates)
            if frameCounter&2!=0:
                fireball.move()
    '''
    for index in range(len(fireSet)): #get locations of each fireball
         fireLoc.append(fireSet[index].origin)
    '''
    for index in range(len(eneSet)): #gets locations of enemies
        eneLoc.append(eneSet[index].location)
        
    for fireball in list(x.origin for x in UserPlayer.myFire):
        if fireball in eneLoc:
            #print "hit"
            eneSet.remove(eneSet[eneLoc.index(fireball)])
            eneLoc.remove(fireball)

    if len(eneSet)!= 0: #If there are any enemies on the map
        for enemy in eneSet: #move Each enemy
            enemy.move(frameCounter)
         
    if UserPlayer.location in eneLoc:
        atker=eneSet[eneLoc.index(UserPlayer.location)]
        UserPlayer.hurt(atker.atk)
    
    if UserPlayer.location in currentMap.warpSet:
        try:
            UserPlayer.location=currentMap.warpDes[currentMap.warpSet.index(UserPlayer.location)]
        except IndexError:
            LogUpdater.messages.append("hey idiot you didn't set a destination!")
            UserPlayer.location=(1,1)
            
    if UserPlayer.location in currentMap.foodSet: #removes food from map and adds food to hungerLev
        currentMap.foodSet.remove(UserPlayer.location)
        LogUpdater.messages.append("*Glup*")
        UserPlayer.health+=35
    
    if UserPlayer.health>150: #resets hungerMes so that hunger messages will show up again
        UserPlayer.mes=1
    elif UserPlayer.health>75 and UserPlayer.health<100:
        UserPlayer.mes=2
    elif UserPlayer.health>50 and UserPlayer.health<75:
        UserPlayer.mes=3
    elif UserPlayer.health>20 and UserPlayer.health<50:
        UserPlayer.mes=4
    elif UserPlayer.health>0 and UserPlayer.health<20:
        UserPlayer.mes=5
    
    if UserPlayer.location in currentMap.orbSet: #removes orb from map and adds orb to orbsCollected
        currentMap.orbSet.remove(UserPlayer.location)
        #actLog.append("You found one of the Orbs!")
        LogUpdater.messages.append("You found one of the Orbs!")
        UserPlayer.orbs+=1
        orbLbl.config(text="Orbs: "+str(UserPlayer.orbs))
        if len(currentMap.orbSet)==0: #checks if the player has collected all of the orbs
            #actLog.append("You found all the Orbs!")
            LogUpdater.messages.append("You found all the Orbs!")
            win()
            
            
    for item in mapcontent: #places approprate tiles on map
        if item in currentMap.wallSet: #this is for placeing each wall tile in the appropriate place
            if listPos<11:#Places walls on top row
               tiles.append(mapScreen.create_image((listPos*30,0), image=wallSp, anchor=NW))
            if listPos>10 and listPos<22: #Places walls on 2nd row
                tiles.append(mapScreen.create_image(((listPos-11)*30,30), image=wallSp, anchor=NW))
            if listPos>21 and listPos<33:#Places walls on 3rd row
                tiles.append(mapScreen.create_image(((listPos-22)*30,60), image=wallSp, anchor=NW))
            if listPos>32 and listPos<44:#Places walls on 4th row
                tiles.append(mapScreen.create_image(((listPos-33)*30,90), image=wallSp, anchor=NW))
            if listPos>43 and listPos<55:#Places walls on 5th row
                tiles.append(mapScreen.create_image(((listPos-44)*30,120), image=wallSp, anchor=NW))
            if listPos>54 and listPos<66:#Places walls on 6th row
                tiles.append(mapScreen.create_image(((listPos-55)*30,150), image=wallSp, anchor=NW))
            if listPos>65 and listPos<77:#Places walls on 7th row
                tiles.append(mapScreen.create_image(((listPos-66)*30,180), image=wallSp, anchor=NW))
            if listPos>76 and listPos<88:#Places walls on 8th row
                tiles.append(mapScreen.create_image(((listPos-77)*30,210), image=wallSp, anchor=NW))
            if listPos>87 and listPos<99:#Places walls on 9th row
                tiles.append(mapScreen.create_image(((listPos-88)*30,240), image=wallSp, anchor=NW))
            if listPos>98 and listPos<110:#Places walls on 10th row
                tiles.append(mapScreen.create_image(((listPos-99)*30,270), image=wallSp, anchor=NW))
            if listPos>109 and listPos<121:#Places walls on 11th row
                tiles.append(mapScreen.create_image(((listPos-110)*30,300), image=wallSp, anchor=NW))
        else:
            if listPos<11:#Places floor tiles on the map (same as wall placing just places floor if there is no wall)
               tiles.append(mapScreen.create_image((listPos*30,0), image=floorSp, anchor=NW))
            if listPos>10 and listPos<22:
                tiles.append(mapScreen.create_image(((listPos-11)*30,30), image=floorSp, anchor=NW))
            if listPos>21 and listPos<33:
                tiles.append(mapScreen.create_image(((listPos-22)*30,60), image=floorSp, anchor=NW))
            if listPos>32 and listPos<44:
                tiles.append(mapScreen.create_image(((listPos-33)*30,90), image=floorSp, anchor=NW))
            if listPos>43 and listPos<55:
                tiles.append(mapScreen.create_image(((listPos-44)*30,120), image=floorSp, anchor=NW))
            if listPos>54 and listPos<66:#Places walls on 6th row
                tiles.append(mapScreen.create_image(((listPos-55)*30,150), image=floorSp, anchor=NW))
            if listPos>65 and listPos<77:#Places walls on 7th row
                tiles.append(mapScreen.create_image(((listPos-66)*30,180), image=floorSp, anchor=NW))
            if listPos>76 and listPos<88:#Places walls on 8th row
                tiles.append(mapScreen.create_image(((listPos-77)*30,210), image=floorSp, anchor=NW))
            if listPos>87 and listPos<99:#Places walls on 9th row
                tiles.append(mapScreen.create_image(((listPos-88)*30,240), image=floorSp, anchor=NW))
            if listPos>98 and listPos<110:#Places walls on 10th row
                tiles.append(mapScreen.create_image(((listPos-99)*30,270), image=floorSp, anchor=NW))
            if listPos>109 and listPos<121:#Places walls on 11th row
                tiles.append(mapScreen.create_image(((listPos-110)*30,300), image=floorSp, anchor=NW))
        
        if item in currentMap.warpSet:#places warp here
            if listPos<11:
               tiles.append(mapScreen.create_image((listPos*30,0), image=warpSp, anchor=NW))
            if listPos>10 and listPos<22:
                tiles.append(mapScreen.create_image(((listPos-11)*30,30), image=warpSp, anchor=NW))
            if listPos>21 and listPos<33:
                tiles.append(mapScreen.create_image(((listPos-22)*30,60), image=warpSp, anchor=NW))
            if listPos>32 and listPos<44:
                tiles.append(mapScreen.create_image(((listPos-33)*30,90), image=warpSp, anchor=NW))
            if listPos>43 and listPos<55:
                tiles.append(mapScreen.create_image(((listPos-44)*30,120), image=warpSp, anchor=NW))
            if listPos>54 and listPos<66:#Places walls on 6th row
                tiles.append(mapScreen.create_image(((listPos-55)*30,150), image=warpSp, anchor=NW))
            if listPos>65 and listPos<77:#Places walls on 7th row
                tiles.append(mapScreen.create_image(((listPos-66)*30,180), image=warpSp, anchor=NW))
            if listPos>76 and listPos<88:#Places walls on 8th row
                tiles.append(mapScreen.create_image(((listPos-77)*30,210), image=warpSp, anchor=NW))
            if listPos>87 and listPos<99:#Places walls on 9th row
                tiles.append(mapScreen.create_image(((listPos-88)*30,240), image=warpSp, anchor=NW))
            if listPos>98 and listPos<110:#Places walls on 10th row
                tiles.append(mapScreen.create_image(((listPos-99)*30,270), image=warpSp, anchor=NW))
            if listPos>109 and listPos<121:#Places walls on 11th row
                tiles.append(mapScreen.create_image(((listPos-110)*30,300), image=warpSp, anchor=NW))
                
        if item in currentMap.foodSet:#places food here so that there is a floor beneath it
            if listPos<11:
               tiles.append(mapScreen.create_image((listPos*30,0), image=foodSp, anchor=NW))
            if listPos>10 and listPos<22:
                tiles.append(mapScreen.create_image(((listPos-11)*30,30), image=foodSp, anchor=NW))
            if listPos>21 and listPos<33:
                tiles.append(mapScreen.create_image(((listPos-22)*30,60), image=foodSp, anchor=NW))
            if listPos>32 and listPos<44:
                tiles.append(mapScreen.create_image(((listPos-33)*30,90), image=foodSp, anchor=NW))
            if listPos>43 and listPos<55:
                tiles.append(mapScreen.create_image(((listPos-44)*30,120), image=foodSp, anchor=NW))
            if listPos>54 and listPos<66:#Places walls on 6th row
                tiles.append(mapScreen.create_image(((listPos-55)*30,150), image=foodSp, anchor=NW))
            if listPos>65 and listPos<77:#Places walls on 7th row
                tiles.append(mapScreen.create_image(((listPos-66)*30,180), image=foodSp, anchor=NW))
            if listPos>76 and listPos<88:#Places walls on 8th row
                tiles.append(mapScreen.create_image(((listPos-77)*30,210), image=foodSp, anchor=NW))
            if listPos>87 and listPos<99:#Places walls on 9th row
                tiles.append(mapScreen.create_image(((listPos-88)*30,240), image=foodSp, anchor=NW))
            if listPos>98 and listPos<110:#Places walls on 10th row
                tiles.append(mapScreen.create_image(((listPos-99)*30,270), image=foodSp, anchor=NW))
            if listPos>109 and listPos<121:#Places walls on 11th row
                tiles.append(mapScreen.create_image(((listPos-110)*30,300), image=foodSp, anchor=NW))
        
        if item in currentMap.orbSet:#places orb here so that there is a floor beneath it
            if listPos<11:
               tiles.append(mapScreen.create_image((listPos*30,0), image=orbSp, anchor=NW))
            if listPos>10 and listPos<22:
                tiles.append(mapScreen.create_image(((listPos-11)*30,30), image=orbSp, anchor=NW))
            if listPos>21 and listPos<33:
                tiles.append(mapScreen.create_image(((listPos-22)*30,60), image=orbSp, anchor=NW))
            if listPos>32 and listPos<44:
                tiles.append(mapScreen.create_image(((listPos-33)*30,90), image=orbSp, anchor=NW))
            if listPos>43 and listPos<55:
                tiles.append(mapScreen.create_image(((listPos-44)*30,120), image=orbSp, anchor=NW))
            if listPos>54 and listPos<66:#Places walls on 6th row
                tiles.append(mapScreen.create_image(((listPos-55)*30,150), image=orbSp, anchor=NW))
            if listPos>65 and listPos<77:#Places walls on 7th row
                tiles.append(mapScreen.create_image(((listPos-66)*30,180), image=orbSp, anchor=NW))
            if listPos>76 and listPos<88:#Places walls on 8th row
                tiles.append(mapScreen.create_image(((listPos-77)*30,210), image=orbSp, anchor=NW))
            if listPos>87 and listPos<99:#Places walls on 9th row
                tiles.append(mapScreen.create_image(((listPos-88)*30,240), image=orbSp, anchor=NW))
            if listPos>98 and listPos<110:#Places walls on 10th row
                tiles.append(mapScreen.create_image(((listPos-99)*30,270), image=orbSp, anchor=NW))
            if listPos>109 and listPos<121:#Places walls on 11th row
                tiles.append(mapScreen.create_image(((listPos-110)*30,300), image=orbSp, anchor=NW))        
        
        if item in currentMap.spawnerSet:#places spawner here so that there is a floor beneath it
            if listPos<11:
               tiles.append(mapScreen.create_image((listPos*30,0), image=spawnSp, anchor=NW))
            if listPos>10 and listPos<22:
                tiles.append(mapScreen.create_image(((listPos-11)*30,30), image=spawnSp, anchor=NW))
            if listPos>21 and listPos<33:
                tiles.append(mapScreen.create_image(((listPos-22)*30,60), image=spawnSp, anchor=NW))
            if listPos>32 and listPos<44:
                tiles.append(mapScreen.create_image(((listPos-33)*30,90), image=spawnSp, anchor=NW))
            if listPos>43 and listPos<55:
                tiles.append(mapScreen.create_image(((listPos-44)*30,120), image=spawnSp, anchor=NW))
            if listPos>54 and listPos<66:#Places walls on 6th row
                tiles.append(mapScreen.create_image(((listPos-55)*30,150), image=spawnSp, anchor=NW))
            if listPos>65 and listPos<77:#Places walls on 7th row
                tiles.append(mapScreen.create_image(((listPos-66)*30,180), image=spawnSp, anchor=NW))
            if listPos>76 and listPos<88:#Places walls on 8th row
                tiles.append(mapScreen.create_image(((listPos-77)*30,210), image=spawnSp, anchor=NW))
            if listPos>87 and listPos<99:#Places walls on 9th row
                tiles.append(mapScreen.create_image(((listPos-88)*30,240), image=spawnSp, anchor=NW))
            if listPos>98 and listPos<110:#Places walls on 10th row
                tiles.append(mapScreen.create_image(((listPos-99)*30,270), image=spawnSp, anchor=NW))
            if listPos>109 and listPos<121:#Places walls on 11th row
                tiles.append(mapScreen.create_image(((listPos-110)*30,300), image=spawnSp, anchor=NW)) 
        try:
            if item == UserPlayer.myAir.location1 or item== UserPlayer.myAir.location2: #places fireballs and places each fireball with correct sprite
                if listPos<11:
                    tiles.append(mapScreen.create_image((listPos*30,0), image=UserPlayer.myAir.img, anchor=NW))
                if listPos>10 and listPos<22:
                    tiles.append(mapScreen.create_image(((listPos-11)*30,30), image=UserPlayer.myAir.img, anchor=NW))
                if listPos>21 and listPos<33:
                    tiles.append(mapScreen.create_image(((listPos-22)*30,60), image=UserPlayer.myAir.img, anchor=NW))
                if listPos>32 and listPos<44:
                    tiles.append(mapScreen.create_image(((listPos-33)*30,90), image=UserPlayer.myAir.img, anchor=NW))
                if listPos>43 and listPos<55:
                    tiles.append(mapScreen.create_image(((listPos-44)*30,120), image=UserPlayer.myAir.img, anchor=NW))
                if listPos>54 and listPos<66:#Places walls on 6th row
                    tiles.append(mapScreen.create_image(((listPos-55)*30,150), image=UserPlayer.myAir.img, anchor=NW))
                if listPos>65 and listPos<77:#Places walls on 7th row
                    tiles.append(mapScreen.create_image(((listPos-66)*30,180), image=UserPlayer.myAir.img, anchor=NW))
                if listPos>76 and listPos<88:#Places walls on 8th row
                    tiles.append(mapScreen.create_image(((listPos-77)*30,210), image=UserPlayer.myAir.img, anchor=NW))
                if listPos>87 and listPos<99:#Places walls on 9th row
                    tiles.append(mapScreen.create_image(((listPos-88)*30,240), image=UserPlayer.myAir.img, anchor=NW))
                if listPos>98 and listPos<110:#Places walls on 10th row
                    tiles.append(mapScreen.create_image(((listPos-99)*30,270), image=UserPlayer.myAir.img, anchor=NW))
                if listPos>109 and listPos<121:#Places walls on 11th row
                    tiles.append(mapScreen.create_image(((listPos-110)*30,300), image=UserPlayer.myAir.img, anchor=NW))
        except AttributeError:
            nothing()
        try:
            fireCheck=list(x.origin for x in UserPlayer.myFire)
            if item in fireCheck: #places fireballs and places each fireball with correct sprite
                if listPos<11:
                    tiles.append(mapScreen.create_image((listPos*30,0), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
                if listPos>10 and listPos<22:
                    tiles.append(mapScreen.create_image(((listPos-11)*30,30), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
                if listPos>21 and listPos<33:
                    tiles.append(mapScreen.create_image(((listPos-22)*30,60), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
                if listPos>32 and listPos<44:
                    tiles.append(mapScreen.create_image(((listPos-33)*30,90), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
                if listPos>43 and listPos<55:
                    tiles.append(mapScreen.create_image(((listPos-44)*30,120), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
                if listPos>54 and listPos<66:#Places walls on 6th row
                    tiles.append(mapScreen.create_image(((listPos-55)*30,150), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
                if listPos>65 and listPos<77:#Places walls on 7th row
                    tiles.append(mapScreen.create_image(((listPos-66)*30,180), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
                if listPos>76 and listPos<88:#Places walls on 8th row
                    tiles.append(mapScreen.create_image(((listPos-77)*30,210), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
                if listPos>87 and listPos<99:#Places walls on 9th row
                    tiles.append(mapScreen.create_image(((listPos-88)*30,240), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
                if listPos>98 and listPos<110:#Places walls on 10th row
                    tiles.append(mapScreen.create_image(((listPos-99)*30,270), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
                if listPos>109 and listPos<121:#Places walls on 11th row
                    tiles.append(mapScreen.create_image(((listPos-110)*30,300), image=UserPlayer.myFire[fireCheck.index(item)].img, anchor=NW))
        except AttributeError:
            nothing()
        try:
            if item in eneLoc: #places enemy
                if listPos<11:
                    tiles.append(mapScreen.create_image((listPos*30,0), image=eneSet[eneLoc.index(item)].img, anchor=NW))
                if listPos>10 and listPos<22:
                    tiles.append(mapScreen.create_image(((listPos-11)*30,30), image=eneSet[eneLoc.index(item)].img, anchor=NW))
                if listPos>21 and listPos<33:
                    tiles.append(mapScreen.create_image(((listPos-22)*30,60), image=eneSet[eneLoc.index(item)].img, anchor=NW))
                if listPos>32 and listPos<44:
                    tiles.append(mapScreen.create_image(((listPos-33)*30,90), image=eneSet[eneLoc.index(item)].img, anchor=NW))
                if listPos>43 and listPos<55:
                    tiles.append(mapScreen.create_image(((listPos-44)*30,120), image=eneSet[eneLoc.index(item)].img, anchor=NW))
                if listPos>54 and listPos<66:#Places walls on 6th row
                    tiles.append(mapScreen.create_image(((listPos-55)*30,150), image=eneSet[eneLoc.index(item)].img, anchor=NW))
                if listPos>65 and listPos<77:#Places walls on 7th row
                    tiles.append(mapScreen.create_image(((listPos-66)*30,180), image=eneSet[eneLoc.index(item)].img, anchor=NW))
                if listPos>76 and listPos<88:#Places walls on 8th row
                    tiles.append(mapScreen.create_image(((listPos-77)*30,210), image=eneSet[eneLoc.index(item)].img, anchor=NW))
                if listPos>87 and listPos<99:#Places walls on 9th row
                    tiles.append(mapScreen.create_image(((listPos-88)*30,240), image=eneSet[eneLoc.index(item)].img, anchor=NW))
                if listPos>98 and listPos<110:#Places walls on 10th row
                    tiles.append(mapScreen.create_image(((listPos-99)*30,270), image=eneSet[eneLoc.index(item)].img, anchor=NW))
                if listPos>109 and listPos<121:#Places walls on 11th row
                    tiles.append(mapScreen.create_image(((listPos-110)*30,300), image=eneSet[eneLoc.index(item)].img, anchor=NW))
        except:
            print "?"

        if item==UserPlayer.location: #places the correct player tile it is always in the center
            if UserPlayer.direction==1:
                tiles.append(mapScreen.create_image((150,150), image=northSp, anchor=NW))
            elif UserPlayer.direction==2:
                tiles.append(mapScreen.create_image((150,150), image=eastSp, anchor=NW))
            elif UserPlayer.direction==3:
                tiles.append(mapScreen.create_image((150,150), image=southSp, anchor=NW))
            elif UserPlayer.direction==4:
                tiles.append(mapScreen.create_image((150,150), image=westSp, anchor=NW))
        listPos+=1
        
    if UserPlayer.health==150 and UserPlayer.mes==1: #sends message if the player is hungry
        LogUpdater.messages.append("I'm ok...")
        UserPlayer.mes+=1
    elif UserPlayer.health==75 and UserPlayer.mes==2:
        LogUpdater.messages.append("Ouch... I'm hurt.")
        UserPlayer.mes+=1
    elif UserPlayer.health==50 and UserPlayer.mes==3:
        LogUpdater.messages.append("I'm very unwell...")
        UserPlayer.mes+=1
    elif UserPlayer.health==20 and UserPlayer.mes==4:
        LogUpdater.messages.append("I'm desparate.")
        UserPlayer.mes+=1
    elif UserPlayer.health==0 or UserPlayer.health<0:
        LogUpdater.messages.append("You have joined the ranks of the dead.")
        
        
    
    hungerMeter.config(text="Health: "+str(UserPlayer.health))#updates health meter
    coolLbl.config(text="Fire Cooldown: "+ str(UserPlayer.activeCooldown))

        

def win(): #Sends you to the Winner's Room and displays the 'You Win!' image
    global currentMap
    UserPlayer.location=(0,0)
    currentMap= loadMap("map2.png")
    LogUpdater.messages.append("Location: "+currentMap.myName)
    UserPlayer.location=currentMap.startLoc
    
    #visScreen.create_image((300,225), image=winSp)
    #drawMap()
      
def nothing(event=0):#meant to do nothing
    nothing=1

def loadMap(currentMap): #Loads map from PNG image
    global eneSet
    global eneLoc
    WALL_COLOR=(0,0,0) #Black pixel is wall
    FOOD_COLOR=(255,0,0) #Red pixel is food
    ORB_COLOR=(0,0,255) #Blue pixel is orb
    PLAYER_COLOR=(0,255,0) #Green pixel is Player Start
    WARP_COLOR=(255,255,0) #Yellow pixel is Warps
    SPAWNER_COLOR=(0,255,255)# Cyan pixels Spawn Enemies
    
    mapName=currentMap.split(".")
    mapName=mapName[0]
    mapDir=os.path.join(directory, "maps/",currentMap)
    
    mapImg=PIL.Image.open(mapDir) #reads map image
    width, height=mapImg.size #gets size of image
    data= list(mapImg.getdata())#gets pixels of image
    if len(data[0])>3:
        for pix in range(len(data)):
            data[pix]=list(data[pix])
            data[pix].pop()
            data[pix]=tuple(data[pix])
    eneSet=[]
    eneLoc=[]
    wallSet=[]
    foodSet=[]
    orbSet=[]
    warpSet=[]
    spawnerSet=[]
    location=[0,0]    
    for tile in data:
        if tile == WALL_COLOR:
            wallSet.append(tuple(location))
        elif tile== FOOD_COLOR:
            foodSet.append(tuple(location))
        elif tile== ORB_COLOR:
            orbSet.append(tuple(location))
        elif tile== WARP_COLOR:
            warpSet.append(tuple(location))
        elif tile== SPAWNER_COLOR:
            spawnerSet.append(tuple(location))
        elif tile== PLAYER_COLOR:
            pLocation=tuple(location)
        
        location[0]+=1
        if location[0]== width:
            location=[0,location[1]+1]
    
    return mapObj(spawnerSet,wallSet, foodSet, orbSet, pLocation, warpSet, mapName)


global actLog
global logObject
logObject=[]

#TKinter Setup
directory = os.path.dirname(os.path.abspath(__file__)) #gets the file path of the program
window = Tk()
window.title("Catacomb Johnson")
window.geometry("800x600")
window.resizable(False, False)
window.configure(background="black")
window.focus_force()
window.iconbitmap(os.path.join(directory, "asset/favicon.ico"))

actLog=[] #holds strings of messages sent to the Action Log
global fireSet
fireSet=[] #holds Fireball Objs
global eneSet
eneSet=[] #holds Enemy Objs

global frameCounter
frameCounter=1000 #Goes to 0 used to set speeds of objects
#player status
hungerLev=200
orbsCollected=0 #number of orbs the player has collected
hungerMes=1 #Makes sure hunger messages only appear once
pDirection=2

#Loads map from image
currentMap=loadMap("map.png")

LogUpdater=LogUpdater()

UserPlayer=Player(hungerLev, hungerMes, pDirection,  orbsCollected, currentMap.startLoc)

#Images
imgN= PIL.Image.open(os.path.join(directory, "asset/north.gif"))
imgS= PIL.Image.open(os.path.join(directory, "asset/south.gif"))
imgE= PIL.Image.open(os.path.join(directory, "asset/east.gif"))
imgW= PIL.Image.open(os.path.join(directory, "asset/west.gif"))

imgWal= PIL.Image.open(os.path.join(directory, "asset/wall.gif"))
imgFlr= PIL.Image.open(os.path.join(directory, "asset/floor.gif"))
imgFud= PIL.Image.open(os.path.join(directory, "asset/food.gif"))
imgOrb= PIL.Image.open(os.path.join(directory, "asset/orb.gif"))

imgFirN=PIL.Image.open(os.path.join(directory, "asset/northFire.gif"))
imgFirE=PIL.Image.open(os.path.join(directory, "asset/eastFire.gif"))
imgFirS=PIL.Image.open(os.path.join(directory, "asset/southFire.gif"))
imgFirW=PIL.Image.open(os.path.join(directory, "asset/westFire.gif"))

imgAir=PIL.Image.open(os.path.join(directory, "asset/airBlast.png"))

imgSkel= PIL.Image.open(os.path.join(directory, "asset/skeleton.gif"))

imgSpawn1=PIL.Image.open(os.path.join(directory, "asset/spawner.png"))
imgSpawn2=PIL.Image.open(os.path.join(directory, "asset/spawner1.png"))

imgWarp=PIL.Image.open(os.path.join(directory, "asset/warp.png"))

imgWin= PIL.Image.open(os.path.join(directory, "asset/win.gif"))

northSp= PIL.ImageTk.PhotoImage(imgN)
southSp= PIL.ImageTk.PhotoImage(imgS) 
eastSp= PIL.ImageTk.PhotoImage(imgE) 
westSp= PIL.ImageTk.PhotoImage(imgW) 

wallSp= PIL.ImageTk.PhotoImage(imgWal) 
floorSp= PIL.ImageTk.PhotoImage(imgFlr) 
foodSp= PIL.ImageTk.PhotoImage(imgFud) 
orbSp= PIL.ImageTk.PhotoImage(imgOrb)

fireNSp= PIL.ImageTk.PhotoImage(imgFirN)
fireESp= PIL.ImageTk.PhotoImage(imgFirE)
fireSSp= PIL.ImageTk.PhotoImage(imgFirS)
fireWSp= PIL.ImageTk.PhotoImage(imgFirW)

airSp=PIL.ImageTk.PhotoImage(imgAir)

skelSp= PIL.ImageTk.PhotoImage(imgSkel) 

warpSp=PIL.ImageTk.PhotoImage(imgWarp)

spawnSp=PIL.ImageTk.PhotoImage(imgSpawn1)

winSp= PIL.ImageTk.PhotoImage(imgWin)

#Music
dungeonMus=os.path.join(directory, "asset/dungeon.wav")

#WIDGETS
visScreen= Canvas(window, width=150, height=150,bg="gray25",bd=2, relief=SUNKEN) #Screen that shows events
visScreen.grid(column=1,row=0,columnspan=2, sticky=NE)

mapScreen= Canvas(window, width=330, height=330, bg="black",bd=2, relief=SUNKEN) #Map Screen used for navigation
mapScreen.grid(column=0, row=0, padx=100, pady=20, sticky=W)

messageBox= Canvas(window, width=600, height=200, bg="black", bd=2, relief=SUNKEN)
messageBox.grid(column=0, row=1, rowspan=10, sticky=S)

hungerMeter= Label(window, text="Food: "+str(UserPlayer.health), fg="white", bg="black")
hungerMeter.grid(column=1, row=4, sticky=W)

orbLbl= Label(window, text="Orbs: 0", fg="white", bg="black")
orbLbl.grid(column=2, row=4, sticky=W)

coolLbl= Label(window, text="Fire Cooldown: "+ str(UserPlayer.activeCooldown), fg="white", bg="black")
coolLbl.grid(column=1,columnspan=2, row=5, sticky=W)

#update first time
update()
LogUpdater.messages.append("Location: "+currentMap.myName)

#Starts music
snd.PlaySound(dungeonMus, snd.SND_ASYNC|snd.SND_LOOP)

#bindings for Action
window.bind('<Up>', UserPlayer.moveFor)
window.bind('<Down>',UserPlayer.moveBak)
window.bind('<Left>', UserPlayer.turnLeft)
window.bind('<Right>', UserPlayer.turnRight)
window.bind('z', UserPlayer.shootFire)
window.bind('x', UserPlayer.airBlast)

window.mainloop()
#stops music after window is closed
snd.PlaySound(None, snd.SND_ASYNC)

