
class point():

    def __init__(self):
        self.__posX = 0
        self.__posY = 0
        self.__lightID = -1
        self.__carID = -1
        self.__lightSignal = -1 #0 if y direc is green, 1 if x direc is green
    '''
    def __init__(self,x,y,lid,cid):
        self.__posX = x
        self.__posY = y
        self.__lightID = lid
        self.__carID = cid
    '''
    def getPosX(self):
        return self.__posX
    def getPosY(self):
        return self.__posY
    def getCarID(self):
        return self.__carID
    def getLightID(self):
        return self.__lightID
    def setCarID(self,carnum):
        self.__carID = carnum
    def setLightID(self,lightnum):
        self.__lightID = lightnum
    def setLightSignal(self,s):
        self.__lightSignal = s
    def getLightSignal(self):
        return self.__lightSignal
    def setCordinate(self,x,y):
        self.__posX = x
        self.__posY = y
