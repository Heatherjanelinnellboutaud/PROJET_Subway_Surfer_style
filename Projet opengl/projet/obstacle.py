import OpenGL.GL as GL
import viewerGL as viewerGL
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
       self.programme = 0

       self.verrou = [None,time.time()]
       self.time_reset = 2

    def add_object(self, obj, ligne,colonne):
        self.lst_obj.append(obj)
        self.program = obj.program


    def mvmt_obstacle(self):
        for obj in self.lst_obj:
            if obj.transformation.translation[2] > -25:
                obj.transformation.translation[2] -= self.vitesse
            else:
                self.vitesse += 0.001
                self.aleatoire(obj)
                

    def aleatoire(self,obj):
        colonne = randint(-1,1)
        while colonne == self.verrou[0] and self.verrou[1] - time.time()<self.time_reset:#temps que la colonne générée est occupée dans la ligne, on régénère une colonne
                    colonne = randint(-1,1)
        self.verrou[0] = colonne
        self.verrou[1] = time.time()
        obj.transformation.translation[0] = 1.6*colonne
        obj.transformation.translation[2] = 25
                
    def collision(self,poisson):
        for palmier in self.lst_obj:
            dist_x = poisson.transformation.translation[0] - palmier.transformation.translation[0]
            #dist_y = poisson.transformation.translation[1] - palmier.transformation.translation[1] + 2.5
            dist_z = poisson.transformation.translation[2] - palmier.transformation.translation[2]

            distance = (dist_x**2 + dist_z**2)**(1/2)
            if distance <= 1 :
               # perte()
                return True

    def draw(self):
        for o in self.lst_obj:
            o.draw()

    def lst_obj(self):
        return self.lst_obj

    