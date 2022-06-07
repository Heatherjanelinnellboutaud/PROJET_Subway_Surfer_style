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





    nombre_objet_cree = 0
    obstacle = ObstacleGL()
    for i in range(5):
        p = Mesh.load_obj('palmier.obj')    
        p.normalize()
        p.apply_matrix(pyrr.matrix44.create_from_scale([3, 3, 3, 1]))
        tr = Transformation3D()
        tr.translation.x = 2
        tr.translation.y = -np.amin(p.vertices, axis=0)[1] 
        tr.translation.z = -5 + 2*nombre_objet_cree 
        tr.rotation_center.z = 0.2
        texture = glutils.load_texture('palmier.jpg')
        op = Object3D(p.load_to_gpu(), p.get_nb_triangles(), program3d_id, texture, tr)
        obstacle.add_object(op)
        nombre_objet_cree += 1
        # viewer.add_object(op)
    viewer.add_object(obstacle)