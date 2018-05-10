"""This file contains a class to form a system from list of planetery bodies. It reads in the planets and uses method to create a simulation for the system """

#Import all necessary libraries
import math
import numpy as np
import copy
from planets import planets
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class system(object):

    #initiate the system with required inputs
    def __init__(self,bodies,noiterations,delta_t):
        self.energies=[]
        self.k=[]
        self.dt=delta_t
        self.iterations=noiterations
        self.bodycount=len(bodies)
        #list of list of bodies ; each list contains a list of bodies at that time iteration
        self.bodies=[([0] * self.bodycount) for i in range(0,noiterations)]
        for i in range (0,self.bodycount):
            self.bodies[0][i]=copy.deepcopy(bodies[i])
            if self.bodies[0][i].name=="Earth":
                self.earthpos=i

    #Method to calculate the acceleration of the bodies using their position for a given iteration of the bodies grid
    def accelerationcalc(self,i):
        for j in range (0,self.bodycount):
            self.bodies[i][j].force=np.zeros(3)
            for n in range(0,self.bodycount):
                if j!=n:
                    #if self.bodies[i][j].name=="satellitem":
                        #print self.bodies[i][j].pos
                        #print self.bodies[i][j].vel
                    self.bodies[i][j].force += (((self.bodies[i][n].mass*self.bodies[i][j].mass)/((np.linalg.norm(self.bodies[i][n].pos-self.bodies[i][j].pos))**3))*(self.bodies[i][n].pos-self.bodies[i][j].pos ))*6.674e-11
            self.bodies[i][j].acc=self.bodies[i][j].force/self.bodies[i][j].mass




    #Method to simulate by filling out all the iteration grids
    def simulate(self):
        self.accelerationcalc(0)
        for i in range(0,self.iterations-1):
            for j in range(0,self.bodycount):
                #changes to method to account for satellite launches
                if self.bodies[i][j].name=="satellitem":
                    if self.dt*i<=31557600*2:
                        self.bodies[i+1][j]= copy.deepcopy(self.bodies[i][j])
                        #self.bodies[i][j].pos=self.bodies[i][self.earthpos].pos+self.bodies[i][j].po
                        boolecount=0
                    else:
                        #if boolecount==0:
                            #self.bodies[i][j].pos=self.bodies[i][self.earthpos].pos+self.bodies[i][j].pos
                            #self.bodies[i][j].vel=self.bodies[i][self.earthpos].pos+self.bodies[i][j].vel
                            #boolecount=1
                        self.bodies[i+1][j]= copy.deepcopy(self.bodies[i][j])
                        self.bodies[i+1][j].pos= self.bodies[i][j].pos+self.bodies[i][j].vel*self.dt+(1./6)*(4*self.bodies[i][j].acc-self.bodies[i-1][j].acc)*self.dt**2
                else:
                    self.bodies[i+1][j]= copy.deepcopy(self.bodies[i][j])
                    if i==0:
                        self.bodies[i+1][j].pos= self.bodies[i][j].pos+self.bodies[i][j].vel*self.dt+((self.bodies[i][j].acc)*self.dt**2)/2.
                    else:
                        self.bodies[i+1][j].pos= self.bodies[i][j].pos+self.bodies[i][j].vel*self.dt+(1./6)*(4*self.bodies[i][j].acc-self.bodies[i-1][j].acc)*self.dt**2
            self.accelerationcalc(i+1)
            for j in range(0,self.bodycount):

                if self.bodies[i][j].name=="satellitem":
                    if self.dt*i<=31557600*2:
                        self.bodies[i+1][j]= copy.deepcopy(self.bodies[i][j])
                    else:
                        self.bodies[i+1][j].vel=self.bodies[i][j].vel + (1./6)*(2*self.bodies[i+1][j].acc+5*self.bodies[i][j].acc-self.bodies[i-1][j].acc)*self.dt
                else:
                    if i==0:
                        self.bodies[i+1][j].vel=self.bodies[i][j].vel + (1./6)*(2*self.bodies[i+1][j].acc+4*self.bodies[i][j].acc)*self.dt
                    else:
                        self.bodies[i+1][j].vel=self.bodies[i][j].vel + (1./6)*(2*self.bodies[i+1][j].acc+5*self.bodies[i][j].acc-self.bodies[i-1][j].acc)*self.dt
            if i%50==0:
                self.gravsim(i)




    #method to calculate energy of system at iteration i and store the iteration and energy in a list of their own
    def gravsim(self,i):
        energy=0
        for j in range (0,self.bodycount):
            self.bodies[i][j].graven=0
            for n in range(0,self.bodycount):
                if j!=n:
                    self.bodies[i][j].graven += ((self.bodies[i][n].mass*self.bodies[i][j].mass)/(np.linalg.norm(self.bodies[i][n].pos-self.bodies[i][j].pos)))*6.674e-11
            self.bodies[i][j].kinen=0.5*self.bodies[i][j].mass*((np.linalg.norm(self.bodies[i][j].vel)**2))
            energy += self.bodies[i][j].graven+self.bodies[i][j].kinen
        self.k.append(i)
        self.energies.append(energy)

    #method to use the list of iterations and corresponding energies to write to a file
    def gravwrite(self,filename):
        fileout = open(filename,"w")
        for i in range(len(self.k)):
            fileout.write(str(self.k[i])+","+str(self.energies[i])+"\n")

    def plotgrav(self):
        plt.plot(self.k,self.energies)
        plt.show()


    def orbitalp(self,planet):
        boolcounte=0
        for i in range (1,self.iterations-1):
            for j in range (self.bodycount):
                if boolcounte==0:
                    if np.sign(self.bodies[i][self.earthpos].pos[1])==np.sign(self.bodies[i+1][self.earthpos].pos[1]):
                        orbitcounte=i
                    else:
                        boolcounte=1
        boolcountp=0
        for i in range (1,self.iterations-1):
            for j in range (self.bodycount):
                if boolcountp==0:
                    if self.bodies[i][j].name==planet:
                        if np.sign(self.bodies[i][j].pos[1])==np.sign(self.bodies[i+1][j].pos[1]):
                            orbitcountp=i
                        else:
                            boolcountp=1
        relper=float(orbitcounte)/float(orbitcountp)
        return relper

    #method to calculate shortest distance between 2 given planets 
    def shordis(self,planet1,planet2):
        pla1loc=10
        pla2loc=10
        shortestdis=0
        for i in range (self.bodycount):
            if self.bodies[0][i].name==planet1:
                pla1loc=i
        for i in range (self.bodycount):
            if self.bodies[0][i].name==planet2:
                pla2loc=i
        for i in range (1,self.iterations):
            if np.linalg.norm(self.bodies[i-1][pla1loc].pos-self.bodies[i-1][pla2loc].pos)>np.linalg.norm(self.bodies[i][pla1loc].pos-self.bodies[i][pla2loc].pos):
                shortestdis=np.linalg.norm(self.bodies[i][pla1loc].pos-self.bodies[i][pla2loc].pos)
        return shortestdis


    def init(self):
        # initialiser for animator
        return self.patches


    def animate(self, i):
        # update the position of each of the circles
        for j in range(0,self.bodycount):
            self.patches[j].center=((self.bodies[i][j].pos[0]),(self.bodies[i][j].pos[1]))
        return self.patches


    def run(self):
        # create plot elements
        fig = plt.figure()
        ax = plt.axes()
        # create list for circles
        self.patches = []

        # adds a circle for each body to the list of circles that shall be animated
        for j in range(0, self.bodycount):
            #print (self.bodies[0][j].pos,self.bodies[0][j].pos)
            self.patches.append(plt.Circle((self.bodies[0][j].pos[0],self.bodies[0][j].pos[1]), self.bodies[0][j].size, color = self.bodies[0][j].colour, animated = True))

        # add circles to axes
        for i in range(0, self.bodycount):
            ax.add_patch(self.patches[i])

        # set up the axes
        ax.axis('scaled')
        ax.set_ylim(-3e11,3e11)
        ax.set_xlim(-3e11,3e11)
        ax.patch.set_facecolor("black")
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        # create the animation
        anim = FuncAnimation(fig, self.animate, init_func = self.init, frames = self.iterations, repeat = True, interval = 25, blit = True)

        plt.show()
