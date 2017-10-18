#!/bin/python3
import time
from Device import car,light
from Map import point
import os

def printMap(c,trafficmap,carlist,lightlist):
    #os.system('clear')
    print ('')
    print ('--------------------------------------------------')
    print ('cycle:',c)
    print ('--------------------------------------------------')
    for j in range(mapsize):
        for i in range(mapsize):
            _carid = trafficmap[i][j].getCarID()
            _lightid = trafficmap[i][j].getLightID()
            if _carid is not -1:
                '''
                print ("")
                print ("Car {0} is at[{1},{2}],direction is {3},velocity is{4}.".format(_carid, \
                                                                                        carlist[_carid].getPosX(), \
                                                                                        carlist[_carid].getPosY(), \
                                                                                        carlist[_carid].getDirection(), \
                                                                                        carlist[_carid].getVelocity()))
                '''
                print ("<>".rjust(3), end="")
            elif _lightid is not -1:
                '''
                print ("")
                print ("Light {0} is at[{1},{2}], x signal is {3}, y signal is {4},light signal is {5}.".format(_lightid, \
                                                                                           lightlist[_lightid].getPosX(), \
                                                                                           lightlist[_lightid].getPosY(), \
                                                                                           lightlist[_lightid].getXLightSignal(), \
                                                                                           lightlist[_lightid].getYLightSignal(), \
                                                                                           trafficmap[i][j].getLightSignal()))
                '''
                if (trafficmap[i][j].getLightSignal()==0):
                    print ("||".rjust(3), end="")
                else:
                    print ("==".rjust(3), end="")
            else:
                print ("+".rjust(3), end="")
        print ("")
        print ("")


carnum = 1
lightnum = 4
mapsize = 30

trafficMap = [ [point() for i in range(mapsize)] for i in range(mapsize) ]
for i in range(mapsize):
    for j in range(mapsize):
        trafficMap[i][j].setCordinate(i,j)

#print (trafficMap[2][5].getPosX())
#car def __init__(self,x,y,devid,maxv,direc,destx,desty,trafficmap):
#light def __init__(self,x,y,devid,r,trafficmap):

car0 = car(3,7,0,3,1,13,17,trafficMap)
light0 = light(20,10,0,5,trafficMap)
light1 = light(20,17,1,7,trafficMap)

cars = []
lights = []
cars.append(car0)
lights.append(light0)
lights.append(light1)

cycles = 0

while cycles<30:
    printMap(cycles,trafficMap,cars,lights)

    cycles+=1

    for l in lights:
        trafficMap = l.updateLight(cycles,trafficMap)
        x = l.getPosX()
        y = l.getPosY()
        #trafficMap[x][y].setLightSignal(l.getXLightSignal())

    for c in cars:
        trafficMap = c.carDecision(trafficMap)

    time.sleep(2)


#end
