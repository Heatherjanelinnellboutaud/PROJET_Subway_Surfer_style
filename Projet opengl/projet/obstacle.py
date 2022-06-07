import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
import time

class ObstacleGL:
    def __init__(self):

       #obj = Object3D(image) 

       self.lst_obj = []
       self.vitesse = 0.2
       self.pox = 0
       self.posy = 0
       self.posz = 25
    
    def add_object(self, obj):
        self.objs.append(obj)

    def mvmt_obstacle(self,vitesse,numero_objet,objet):
        
        self.vitesse = vitesse
        self.numero_objet = numero_objet
        if self.objs[numero_objet-1].transformation.translation[2] >= -25:
            self.objs[numero_objet-1].transformation.translation -= \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, vitesse]))
        else:
            self.lst_obj.pop(objet)

    