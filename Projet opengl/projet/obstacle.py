import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
import time

class ObstacleGL:
    def __init__(self):

       self.lst_obj = []
       self.numero_objet = 0
       self.vitesse = 0.2
       self.pox = 0
       self.posz = 25

    def add_object(self, obj):
        self.lst_obj.append(obj)

    def mvmt_obstacle(self,vitesse,objet):
        
        self.vitesse = vitesse
        if self.lst_obj[self.lst_obj.index(objet)].transformation.translation[2] >= -25:
            self.lst_obj[self.lst_obj.index(objet)].transformation.translation -= \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.lst_obj[0].transformation.rotation_euler), pyrr.Vector3([0, 0, vitesse]))
            print(self.lst_obj[numero_objet-1].transformation.translation)
        else:
            self.lst_obj.pop(objet)

    def draw(self):
        for o in self.lst_obj:
            o.draw()

    