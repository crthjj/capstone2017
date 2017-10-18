#!/usr/bin/python3
import json
from Map import point

directionStr = ['North','East','South','West']

class trafficDevice():

    __deviceID = -1
    __posX = -1
    __posY = -1

    def __init__(self,x,y,devid):
        self.__posX = x
        self.__posY = y
        self.__deviceID = devid

    def getPosX(self):
        return self.__posX
    def getPosY(self):
        return self.__posY
    def getDeviceID(self):
        return self.__deviceID
    def setPosX(self,x):
        self.__posX = x
    def setPosY(self,y):
        self.__posY = y
    def setDeviceID(self,devid):
        self.__deviceID = devid

class light(trafficDevice):
    __xLightSignal = -1
    __yLightSignal = -1
    __lightRule = -1
    __curCycle = -1

    def __init__(self,x,y,devid,r,trafficmap):
        trafficDevice.__init__(self,x,y,devid)
        self.__lightRule = r
        self.__xLightSignal = 0
        self.__yLightSignal = 1
        trafficmap[x][y].setLightID(devid)
        trafficmap[x][y].setLightSignal(0)#0 if x is red, y is green

    def updateLight(self,curcycle,trafficmap):
        self.__curCycle = curcycle
        if (int(self.__curCycle/self.__lightRule)%2==0):
            self.__xLightSignal = 1
            self.__yLightSignal = 0
            trafficmap[self.getPosX()][self.getPosY()].setLightSignal(1)
            #print ("light{0} changes, curcycle:{1},light signal:{2},light rule:{3}.".format(self.getDeviceID(),self.__curCycle,self.__xLightSignal,self.__lightRule))
            return trafficmap
        else:
            self.__xLightSignal = 0
            self.__yLightSignal = 1
            trafficmap[self.getPosX()][self.getPosY()].setLightSignal(0)
            #print ("light{0} changes, curcycle:{1},light signal:{2},light rule:{3}.".format(self.getDeviceID(),self.__curCycle,self.__xLightSignal,self.__lightRule))
            return trafficmap


    def getXLightSignal(self):
        return self.__xLightSignal
    def getYLightSignal(self):
        return self.__yLightSignal
    '''
    def getNextSignal(self):
        if (((self.__curCycle+1)/self.__lightRule)%2==0):
            return 1
        else:
            return 0
    '''

class car(trafficDevice):
    __maxvelocity = 0
    __velocity = 0
    __direction = -1
    __destPosX = -1
    __destPosY = -1
    __arriveDest = 0

    def __init__(self,x,y,devid,maxv,direc,destx,desty,trafficmap):
        trafficDevice.__init__(self,x,y,devid)
        self.__maxvelocity = maxv
        self.__velocity = 0
        self.__direction = direc
        self.__destPosX = destx
        self.__destPosY = desty
        self.__arriveDest = 0
        trafficmap[x][y].setCarID(devid)

    def getVelocity(self):
        return self.__velocity
    def getDirection(self):
        return self.__direction
    def getDestPosX(self):
        return self.__destPosX
    def getDestPosY(self):
        return self.__destPosY
    def sendMsg(self):
        msg = [{'posX': self.getPosX(), 'posY': self.getPosY(),
                'velocity': self.__velocity, 'direction': self.__direction}]
        json = json.dumps(msg)
        return json

    def setDirection(self):
        if self.getPosX()<self.__destPosX:
            self.__direction = 1
        elif self.getPosX()>self.__destPosX:
            self.__direction = 3
        elif self.getPosX()==self.__destPosX and self.getPosY()>self.__destPosY:
            self.__direction = 0
        elif self.getPosX()==self.__destPosX and self.getPosY()<self.__destPosY:
            self.__direction = 2
        else:
            self.__arriveDest = 1
            print ("Car {0} has arrived at destination.")

        #print ("Car {0}\'s direction is {1}".format(self.__deviceID,directionStr[self.__direction]))
        #print ("Current position is [{0},{1}]".format(self.__posX,self.__posY))

    def setVelocity(self,predictTrafficMap):
        _maxV = 0
        if self.__direction == 0:
            _maxV = (self.getposY()-self.__destPosY) if ((self.getPosY()-self.__destPosY)<self.__maxvelocity) else self.__maxvelocity
        elif self.__direction == 1:
            _maxV = (self.__destPosX-self.getPosX()) if ((self.__destPosX-self.getPosX())<self.__maxvelocity) else self.__maxvelocity
        elif self.__direction == 2:
            _maxV = (self.__destPosY-self.getPosY()) if ((self.__destPosY-self.getPosY())<self.__maxvelocity) else self.__maxvelocity
        elif self.__direction == 3:
            _maxV = (self.getPosX()-self.__destPosX) if ((self.getPosX()-self.__destPosX)<self.__maxvelocity) else self.__maxvelocity

        for i in range(1,_maxV+1):
            if self.__direction==0:
                if predictTrafficMap[self.getPosX()][self.getPosY()-i].getLightSignal() is 1: #y is red
                    self.__velocity = i-1
                    return
            elif self.__direction==1:
                if predictTrafficMap[self.getPosX()+i][self.getPosY()].getLightSignal() is 0: #x is red
                    self.__velocity = i-1
                    return
            elif self.__direction==2:
                if predictTrafficMap[self.getPosX()][self.getPosY()+i].getLightSignal() is 1: #y is red
                    self.__velocity = i-1
                    return
            elif self.__direction==3:
                if predictTrafficMap[self.getPosX()-i][self.getPosY()].getLightSignal() is 0: #x is red
                    self.__velocity = i-1
                    return

        self.__velocity = _maxV
        return

    def carDecision(self,predictTrafficMap):
        predictTrafficMap[self.getPosX()][self.getPosY()].setCarID(-1)

        self.setDirection()
        self.setVelocity(predictTrafficMap)

        if self.__direction==0:
            self.setPosY(self.getPosY() - self.__velocity)
        elif self.__direction==1:
            self.setPosX(self.getPosX() + self.__velocity)
        elif self.__direction==2:
            self.setPosY(self.getPosY() + self.__velocity)
        else:
            self.setPosX(self.getPosX() - self.__velocity)

        predictTrafficMap[self.getPosX()][self.getPosY()].setCarID(self.getDeviceID())
        return predictTrafficMap
