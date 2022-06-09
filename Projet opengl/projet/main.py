from random import randint
from viewerGL import ViewerGL
from obstacle import ObstacleGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr

def main():
    viewer = ViewerGL()
    
    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')

    
     

# PERSONNAGE --------------------------------------------------
    m = Mesh.load_obj('poisson.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -23
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('poisson.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

# PALMIERS ---------------------------------------------------------
    nbr_ligne_obstacle = 0
    obstacle = ObstacleGL()
    for i in range(5):
        colonne = []
        double = randint(0,2)#une chance sur trois de mettre 2 palmiers sur une ligne
        if double != 2:
            nbr_palm_ligne = 1
            colonne.append(randint(-1,1))
        else:
            nbr_palm_ligne = 2
            premiere_colonne = randint(-1,1)
            colonne.append(premiere_colonne)
            superposition = True
            while superposition == True:
                deuxieme_colonne = randint(-1,1)
                if deuxieme_colonne != premiere_colonne:
                    colonne.append(deuxieme_colonne)
                    superposition = False


        for palmier in range(nbr_palm_ligne):
            p = Mesh.load_obj('palmier.obj')    
            p.normalize()
            p.apply_matrix(pyrr.matrix44.create_from_scale([3, 3, 3, 5]))
            tr = Transformation3D()
            tr.translation.x = 1.5*colonne[palmier-1]
            tr.translation.y = -np.amin(p.vertices, axis=0)[1] 
            tr.translation.z = 10*nbr_ligne_obstacle 
            tr.rotation_center.z = 0.2
            texture = glutils.load_texture('palmier.jpg')
            op = Object3D(p.load_to_gpu(), p.get_nb_triangles(), program3d_id, texture, tr)
            obstacle.add_object(op)

        colonne_caillou = randint(-1,1)

        if colonne_caillou not in colonne:
            m = Mesh.load_obj('rocher.obj')    
            m.normalize()
            m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
            tr = Transformation3D()
            tr.translation.x = 1.5*colonne_caillou
            tr.translation.y = -np.amin(m.vertices, axis=0)[1]
            tr.translation.z = 10*(nbr_ligne_obstacle)
            tr.rotation_center.z = 0.2
            texture = glutils.load_texture('rocher.jpg')
            o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
            obstacle.add_object(o)

        nbr_ligne_obstacle += 1
            

    viewer.add_object(obstacle)

    

# ROCHER ---------------------------------------------------------

    


    m = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('eau.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [-2.5,0.01, -25], [2.5,0.01, -25], [2.5,0.01, 25], [-2.5,0.01, 25]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('sable.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    viewer.run()
    

    


if __name__ == '__main__':
    main()