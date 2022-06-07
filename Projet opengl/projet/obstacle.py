import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D, Transformation3D
import time
from random import randint

class ObstacleGL:
    def __init__(self):

       self.lst_obj = []
       self.numero_objet = 0
       self.vitesse = 0.2
       self.pox = 0
       self.posz = 25
       self.programme = 0

    def add_object(self, obj):
        self.lst_obj.append(obj)
        self.program = obj.program

    def mvmt_obstacle(self):
        for obj in self.lst_obj:
            if obj.transformation.translation[2] >= -25:
                obj.transformation.translation[2] -= self.vitesse
            else:
                tr = Transformation3D()
                colonne = randint(-1,1)
                obj.transformation.translation[2] = 25
                self.vitesse += 0.001
                tr.translation.x = 1.6*colonne
                

    def draw(self):
        for o in self.lst_obj:
            o.draw()

    def lst_obj(self):
        return self.lst_obj

    