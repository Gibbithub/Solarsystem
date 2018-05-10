import math
import copy
import numpy as np
from planets import planets
from system import system



def main():
    #planet=input("input the name of the file with all the planetary bodies you want to simulate: ")
    filein = open("planetinfo.txt","r")
    planet=[]
    for line in filein.readlines():
        tokens = line.split(",")
        for i in range (1,5):
            tokens[i]=float(tokens[i])
        planet.append(tokens)
    filein.close()

    for i in range (len(planet)):
        for j in range (5):
            if j==1:
                planet[i][j]=np.array([planet[i][j],0.,0.])
            if j==2:
                planet[i][j]=np.array([0.,planet[i][j],0.])

    planetsobj=[]
    for i in range (0,len(planet)):
        x=planets(planet[i])
        planetsobj.append(x)
    satellite=["satellitem",np.array([1.496e11+6371,0.,0]),np.array([2000.,32000.,0]),10e3,3e9,"c"]
    planetsobj.append(planets(satellite))


    mysys=system(planetsobj,10000,20000)
    mysys.simulate()
    print mysys.orbitalp("Mars")
    print mysys.shordis("Earth","satellitem")
    mysys.run()
    mysys.plotgrav()
    #mysys.gravwrite("test.txt")

main()
