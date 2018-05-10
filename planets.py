import math
import numpy as np
import copy


class planets(object):

    def __init__(self,attributes):
        self.vel=attributes[2]
        self.name=attributes[0]
        self.pos=attributes[1]
        self.mass=attributes[3]
        self.force=np.zeros(3)
        self.acc=np.zeros(3)
        self.colour=attributes[5]
        self.size=attributes[4]
        self.graven=0
        self.kinen=0
        self.orbper=0
