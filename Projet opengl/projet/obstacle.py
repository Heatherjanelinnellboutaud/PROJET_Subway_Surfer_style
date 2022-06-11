import OpenGL.GL as GL
import viewerGL as ViewerGL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D, Transformation3D,Text
import time
from random import randint
import glutils


class ObstacleGL:
    def __init__(self):

       self.lst_obj = []
       self.numero_objet = 0
       self.vitesse = 0.2
       self.program = 0

       self.verrou = [None,time.time()]
       self.time_reset = 2

    def add_object(self, obj):
        self.lst_obj.append(obj)
        self.program = obj.program

        """if type == "p":
            self.lst_obj.append(obj)
            self.lst_palmier.append(obj)
            self.program = obj.program
        if type == "c":
            self.lst_obj.append(obj)
            self.lst_caillou.append(obj)
            self.program = obj.program"""


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
        for obstacle in self.lst_obj:
            if obstacle.typ == "palmier":
                dist_x = poisson.transformation.translation[0] - obstacle.transformation.translation[0]
                dist_z = poisson.transformation.translation[2] - obstacle.transformation.translation[2]

                distance = (dist_x**2 + dist_z**2)**(1/2)
                if distance <= 1 :
                    print("perdu palmier")
                    return True
            if obstacle.typ == "caillou":
                dist_x = poisson.transformation.translation[0] - obstacle.transformation.translation[0]
                dist_y = poisson.transformation.translation[1] - obstacle.transformation.translation[1]
                dist_z = poisson.transformation.translation[2] - obstacle.transformation.translation[2]
                distance = (dist_x**2 + dist_y**2 + dist_z**2)**(1/2)
                if distance <= 1 :
                    print("perdu caillou")
                    return True

    def draw(self):
        for o in self.lst_obj:
            o.draw()

    def lst_obj(self):
        return self.lst_obj

    