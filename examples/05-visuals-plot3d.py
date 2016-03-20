# pylint: disable=no-member
""" a simple visuals for 3D plot """

import numpy as np
import sys

from vispy import app, gloo, visuals, scene

# Define a simple vertex shader. We use $template variables as placeholders for
# code that will be inserted later on.
vertex_shader = """
void main()
{
    vec4 visual_pos = vec4($position, 1);
    vec4 doc_pos = $visual_to_doc(visual_pos);

    gl_Position = $doc_to_render(doc_pos);
}
"""

fragment_shader = """
void main() {
  gl_FragColor = $color;
}
"""


# now build our visuals
class Plot3DVisual(visuals.Visual):
    """ template """

    def __init__(self, x, y, z):
        """ plot 3D """
        visuals.Visual.__init__(self, vertex_shader, fragment_shader)

        # build Vertices buffer
        data = np.c_[x, y, z]
        v = gloo.VertexBuffer(data.astype(np.float32))

        # bind data
        self.shared_program.vert['position'] = v
        self.shared_program.frag['color'] = (1.0, 0.0, 0.0, 1.0)

        # config
        self.set_gl_state('opaque')
        self._draw_mode = 'line_strip'

    def _prepare_transforms(self, view):
        """ This method is called when the user or the scenegraph has assigned
        new transforms to this visual """
        # Note we use the "additive" GL blending settings so that we do not
        # have to sort the mesh triangles back-to-front before each draw.
        tr = view.transforms
        view_vert = view.view_program.vert
        view_vert['visual_to_doc'] = tr.get_transform('visual', 'document')
        view_vert['doc_to_render'] = tr.get_transform('document', 'render')


# build your visuals, that's all
Plot3D = scene.visuals.create_visual_node(Plot3DVisual)

# The real-things : plot using scene
# build canvas
canvas = scene.SceneCanvas(keys='interactive', show=True)

# Add a ViewBox to let the user zoom/rotate
view = canvas.central_widget.add_view()
view.camera = 'turntable'
view.camera.fov = 50
view.camera.distance = 5

# data
N = 1000
x = np.sin(np.linspace(-10, 10, N)*np.pi)
y = np.cos(np.linspace(-10, 10, N)*np.pi)
z = np.linspace(-2, 2, N)

# plot ! note the parent parameter
p1 = Plot3D(x, y, z, parent=view.scene)

# run
if __name__ == '__main__':
    if sys.flags.interactive != 1:
        app.run()
