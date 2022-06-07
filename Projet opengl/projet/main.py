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
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    

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
    nombre_objet_cree = 0
    obstacle_p = ObstacleGL()
    for i in range(8):
        colonne = randint(-1,1)
        p = Mesh.load_obj('palmier.obj')    
        p.normalize()
        p.apply_matrix(pyrr.matrix44.create_from_scale([3, 3, 3, 1]))
        tr = Transformation3D()
        tr.translation.x = 1.6*colonne
        tr.translation.y = -np.amin(p.vertices, axis=0)[1] 
        tr.translation.z = -5 + 5*nombre_objet_cree 
        tr.rotation_center.z = 0.2
        texture = glutils.load_texture('palmier.jpg')
        o_p = Object3D(p.load_to_gpu(), p.get_nb_triangles(), program3d_id, texture, tr)
        obstacle_p.add_object(o_p)
        nombre_objet_cree += 1
        # viewer.add_object(op)
    viewer.add_object(obstacle_p)

    

# ROCHER ---------------------------------------------------------
    obstacle_r = ObstacleGL()

    r = Mesh.load_obj('rocher.obj')    
    r.normalize()
    r.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(r.vertices, axis=0)[1]
    tr.translation.z = 10
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('rocher.jpg')
    o_r = Object3D(r.load_to_gpu(), r.get_nb_triangles(), program3d_id, texture, tr)
    obstacle_r.add_object(o_r)
    nombre_objet_cree += 1
    viewer.add_object(obstacle_r)

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

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    o = Text('', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)

    viewer.run()
    
    


if __name__ == '__main__':
    main()