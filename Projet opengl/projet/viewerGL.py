#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
from obstacle import ObstacleGL
import time

class ViewerGL:
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.touch = {}
        self.vitesse = 0
        self.numero_objet = 0
        self.flag = 1
        
        self.vad = 0 # va a droite
        self.vag = 0 # va a gauche

    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()

            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                if isinstance(obj, ObstacleGL):
                    obj.mvmt_obstacle(0.2)

                obj.draw()

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()        

    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)

        # GAUCHE
        if key == glfw.KEY_LEFT and action == glfw.PRESS and self.vad == 0:
            if self.objs[0].transformation.translation[0] < 0:
                while self.objs[0].transformation.translation[0] < 0:
                    self.objs[0].transformation.translation += pyrr.Vector3([0.1, 0, 0])
                    self.vag = 1
                self.vag = 0
            elif self.objs[0].transformation.translation[0] < 1.5 and self.objs[0].transformation.translation[0] >= 0:
                while self.objs[0].transformation.translation[0] < 1.5:
                    self.objs[0].transformation.translation += pyrr.Vector3([0.1, 0, 0])
                    self.vag = 1
                self.vag = 0

        # DROITE
        if key == glfw.KEY_RIGHT and action == glfw.PRESS and self.vag == 0:
            if self.objs[0].transformation.translation[0] > 0:
                while self.objs[0].transformation.translation[0] > 0:
                    self.objs[0].transformation.translation -= pyrr.Vector3([0.1, 0, 0])
                    self.vad = 1
                self.vad = 0
            elif self.objs[0].transformation.translation[0] > -1.5 and self.objs[0].transformation.translation[0] <= 0:
                while self.objs[0].transformation.translation[0] > -1.5:
                    self.objs[0].transformation.translation -= pyrr.Vector3([0.1, 0, 0])
                    self.vad = 1
                self.vad = 0
        self.touch[key] = action
                
    def add_object(self, obj):
        self.objs.append(obj)

    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key(self):
        
        self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
        self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 5])

# SAUT --------------------------------------------------------
        if glfw.KEY_SPACE in self.touch and self.flag == 1:
                self.saut_montee()
        if glfw.KEY_SPACE in self.touch and self.flag == 0:
            self.saut_descente()
 
    def saut_montee(self):
        if self.objs[0].transformation.translation[1] <= 3:
            tmp = (4-self.objs[0].transformation.translation[1])*0.05
            self.objs[0].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, tmp, 0]))
        else:
            self.flag = 0

    def saut_descente(self):
        if self.objs[0].transformation.translation[1] >= 1:
            tmp = ((4-0.8)*0.05)-((self.objs[0].transformation.translation[1]-0.8)*0.05)
            self.objs[0].transformation.translation -= \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, tmp, 0]))
        else:
            del self.touch[glfw.KEY_SPACE]
            self.flag = 1