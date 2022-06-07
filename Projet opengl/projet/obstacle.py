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
                
    def collision(self,poisson):
        for palmier in self.lst_obj:
            dist_x = poisson.transformation.translation[0] - palmier.transformation.translation[0]
            #dist_y = poisson.transformation.translation[1] - palmier.transformation.translation[1] + 2.5
            dist_z = poisson.transformation.translation[2] - palmier.transformation.translation[2]

            distance = (dist_x**2 + dist_z**2)**(1/2)
            if distance <= 1 :
                print("perdu sale merde")

    def draw(self):
        for o in self.lst_obj:
            o.draw()

    def lst_obj(self):
        return self.lst_obj

    