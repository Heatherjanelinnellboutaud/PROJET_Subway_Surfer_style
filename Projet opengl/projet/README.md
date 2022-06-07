# PROJET_Subway_Surfer_style

Ceci est notre super projet !!!!

viewer gl
l 111

        if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
            if self.objs[0].transformation.translation[2] <= 25:
                self.objs[0].transformation.translation += \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.1]))
        if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
            if self.objs[0].transformation.translation[2] >= 25:
                self.objs[0].transformation.translation -= \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.1]))

main remplacer stego par poisson

main hauteur sable plus basse

