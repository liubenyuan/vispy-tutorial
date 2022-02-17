import sys

from vispy import scene
from vispy.geometry import create_cube
from vispy.scene.visuals import Cube


canvas = scene.SceneCanvas(
    keys="interactive", size=(800, 600), show=True, bgcolor=(0.5, 0.5, 0.5)
)

view = canvas.central_widget.add_view()

vertices, _, _ = create_cube()

RGB_f = vertices["color"]
RGB_f[..., 3] *= 0.5

cube1 = Cube(vertex_colors=RGB_f, parent=view.scene, size=0.5)
axis = scene.visuals.XYZAxis(parent=view.scene)

view.camera = "turntable"
view.camera.fov = 45

if __name__ == "__main__" and sys.flags.interactive == 0:
    canvas.app.run()
