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

    def mvmt_obstacle(self,vitesse):
        for obj in self.lst_obj:
            self.vitesse = vitesse
            if obj.transformation.translation[2] >= -25:
                obj.transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.lst_obj[0].transformation.rotation_euler), pyrr.Vector3([0, 0, vitesse]))
                print(obj.transformation.translation)
            else:
                tr = Transformation3D()
                colonne = randint(-1,1)
                obj.transformation.translation[2] = 25
                tr.translation.x = 1.6*colonne
    def draw(self):
        for o in self.lst_obj:
            o.draw()

    def lst_obj(self):
        return self.lst_obj

    