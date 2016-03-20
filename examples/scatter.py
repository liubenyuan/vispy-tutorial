# pylint: disable=no-member
""" scatter using MarkersVisual """

import numpy as np
import sys

from vispy import app, visuals, scene


# build your visuals, that's all
Scatter3D = scene.visuals.create_visual_node(visuals.MarkersVisual)

# The real-things : plot using scene
# build canvas
canvas = scene.SceneCanvas(keys='interactive', show=True)

# Add a ViewBox to let the user zoom/rotate
view = canvas.central_widget.add_view()
view.camera = 'turntable'
view.camera.fov = 45
view.camera.distance = 500

# data
n = 500
pos = np.zeros((n, 3))
colors = np.ones((n, 4), dtype=np.float32)
radius, theta, dtheta = 1.0, 0.0, 10.5 / 180.0 * np.pi
for i in range(500):
    theta += dtheta
    x = 0.0 + radius * np.cos(theta)
    y = 0.0 + radius * np.sin(theta)
    z = 1.0 * radius
    r = 10.1 - i * 0.02
    radius -= 0.45
    pos[i] = x, y, z
    colors[i] = (i/500, 1.0-i/500, 0, 0.8)

# plot ! note the parent parameter
p1 = Scatter3D(parent=view.scene)
p1.set_gl_state('translucent', blend=True, depth_test=True)
p1.set_data(pos, face_color=colors, symbol='o', size=10,
            edge_width=0.5, edge_color='blue')

# run
if __name__ == '__main__':
    if sys.flags.interactive != 1:
        app.run()
