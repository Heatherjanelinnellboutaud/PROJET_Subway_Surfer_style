#!/usr/bin/env python3

from tkinter import LEFT, RIGHT
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from obstacle import ObstacleGL
import glutils,time
from random import randint
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import mouse

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
        glfw.set_window_pos(self.window,100,100)
        self.position_fenetre = glfw.get_window_pos(self.window)
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
        self.vie = 1
        self.mvmt_gauche = False
        self.mvmt_droite = False
        self.game_on = False
        
        self.pos = 0
        self.pos_init = 0

        self.vad = 0 # va a droite
        self.vag = 0 # va a gauche

    """def perte(self):
            programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
            vao = Text.initalize_geometry()
            texture = glutils.load_texture('fontB.jpg')
            o = Text('Perdu !!!', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
            ViewerGL.add_object(self,o)"""
    def run(self):
        program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')

        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self.perdu()
            if self.vie == 1:
                self.update_key()
            for obj in self.objs:
                if self.objs.index(obj) != 1:
                    if self.vie == 0:
                        self.objs[0] = self.objs[1]
                    GL.glUseProgram(obj.program)
                    if isinstance(obj, Object3D):
                        self.update_camera(obj.program)
                    if isinstance(obj, ObstacleGL) and self.vie == 1 and self.game_on == True:
                        obj.mvmt_obstacle()
                        collision = obj.collision(self.objs[0])
                        if collision == True:
                            self.collision()
                        if self.objs[0].transformation.translation[2] <= -25:
                            self.objs[1].transformation.translation[0] = self.objs[0].transformation.translation[0]
                            self.objs[1].transformation.translation[2] = self.objs[0].transformation.translation[2]
                            self.objs.pop(-1)
                            self.vie = 0
                            
                            
                    obj.draw()

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events() 

    def perdu(self):
        if self.vie == 0:
            programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
            vao = Text.initalize_geometry()
            texture = glutils.load_texture('fontB.jpg')
            o = Text('Perdu', np.array([0.1, -0.1], np.float32), np.array([0.2, 0.1], np.float32), vao, 2, programGUI_id, texture)
            o.draw()

    def collision(self):
           self.objs[1].transformation.translation[2] += \
        pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.2]))

    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)

        """# GAUCHE
        if key == glfw.KEY_LEFT and action == glfw.PRESS and self.vad == 0:
            if self.objs[0].transformation.translation[0] < 0:
                while self.objs[0].transformation.translation[0] < 0:
                    d = self.objs[0].transformation.translation[0] 
                    d += 0.1
                    self.objs[0].transformation.translation[0] = round(d,1)
                    self.vag = 1
                self.vag = 0
            elif self.objs[0].transformation.translation[0] < 1.5 and self.objs[0].transformation.translation[0] >= 0:
                while self.objs[0].transformation.translation[0] < 1.5:
                    d = self.objs[0].transformation.translation[0] 
                    d += 0.1
                    self.objs[0].transformation.translation[0] = round(d,1)
                    self.vag = 1
                self.vag = 0

        # DROITE
        if key == glfw.KEY_RIGHT and action == glfw.PRESS and self.vag == 0:
            if self.objs[0].transformation.translation[0] > 0:
                while self.objs[0].transformation.translation[0] > 0:
                    d = self.objs[0].transformation.translation[0] 
                    d -= 0.1
                    self.objs[0].transformation.translation[0] = round(d,1)
                    self.vad = 1
                self.vad = 0
            elif self.objs[0].transformation.translation[0] > -1.5 and self.objs[0].transformation.translation[0] <= 0:
                while self.objs[0].transformation.translation[0] > -1.5:
                    d = self.objs[0].transformation.translation[0] 
                    d -= 0.1
                    self.objs[0].transformation.translation[0] = round(d,1)
                    self.vad = 1
                self.vad = 0"""
        if self.game_on == True:
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

        if self.game_on == True:      
    # SAUT --------------------------------------------------------
            if glfw.KEY_SPACE in self.touch and self.flag == 1:
                    self.saut_montee()
            if glfw.KEY_SPACE in self.touch and self.flag == 0:
                self.saut_descente()
    # Gauche --------------------------------------------------------
            if glfw.KEY_LEFT in self.touch and self.pos != -1 and self.mvmt_droite == False:
                self.gauche()
    # Droite --------------------------------------------------------
            if glfw.KEY_RIGHT in self.touch and self.pos != 1 and self.mvmt_gauche == False:
                self.droite()
    # Clic sur play pour démarrer le jeu -------------------------
        if mouse.is_pressed(LEFT): 
            position_souris = mouse.get_position()
            if 750 <= position_souris[0] <= 900 and 100 <= position_souris[1] <= 130:
                self.clic()
#  bas gauche (750,130)  haut droite (900,100)
        

    def gauche(self):
        if abs(self.pos_init-self.objs[0].transformation.translation[0])<1.6:
            self.mvmt_gauche = True
            self.objs[0].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.1, 0, 0]))
        else:
            if self.pos == 0:
                self.pos = -1
            else:
                self.pos = 0
            self.pos_init = self.objs[0].transformation.translation[0]
            self.mvmt_gauche = False
            del self.touch[glfw.KEY_LEFT]

    def droite(self):
        if abs(self.pos_init-self.objs[0].transformation.translation[0])<1.6:
            self.mvmt_droite = True
            self.objs[0].transformation.translation -= \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.1, 0, 0]))
        else:
            if self.pos == 0:
                self.pos = 1
            else:
                self.pos = 0
            self.pos_init = self.objs[0].transformation.translation[0]
            self.mvmt_droite = False
            del self.touch[glfw.KEY_RIGHT]
 
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

    def collision(self):
        self.objs[0].transformation.translation -= \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.2]))

    def clic(self):
        self.game_on = True