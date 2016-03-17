# pylint: disable=invalid-name, no-member, unused-argument
""" basic demo using shaders
http://ipython-books.github.io/featured-06/
"""

import numpy as np
from vispy import app, gloo
from vispy.util.transforms import perspective, translate, rotate

vertex = """
uniform mat4   u_model;         // Model matrix
uniform mat4   u_view;          // View matrix
uniform mat4   u_projection;    // Projection matrix
attribute vec3 a_position;
void main()
{
    gl_Position = u_projection * u_view * u_model * vec4(a_position, 1.0);
}
"""

# The other shader we need to create is the fragment shader.
# It lets us control the pixels' color.
fragment = """
void main()
{
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
"""


class Canvas(app.Canvas):

    def __init__(self, data, theta=37.5, phi=75, z=6):
        # In order to display a window, we need to create a Canvas.
        app.Canvas.__init__(self, size=(800, 400), title='plot3d',
                            keys='interactive')

        # build shader program
        prog = gloo.Program(vert=vertex, frag=fragment)

        # config
        view = np.eye(4, dtype=np.float32)
        model = np.eye(4, dtype=np.float32)
        projection = np.eye(4, dtype=np.float32)

        view = translate((0, 0, -z))
        prog['u_model'] = model
        prog['u_view'] = view
        prog['u_projection'] = projection
        prog['a_position'] = data

        # bind
        self.program = prog
        self.theta = theta
        self.phi = phi

        # config
        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.set_clear_color('white')
        gloo.set_state('opaque')

        # show the canvas
        self.show()

    def on_resize(self, event):
        """
        We create a callback function called when the window is being resized.
        Updating the OpenGL viewport lets us ensure that
        Vispy uses the entire canvas.
        """
        gloo.set_viewport(0, 0, *event.physical_size)
        ratio = event.physical_size[0] / float(event.physical_size[1])
        self.program['u_projection'] = perspective(45.0, ratio, 2.0, 10.0)

    def on_draw(self, event):
        gloo.clear()
        model = np.dot(rotate(self.theta, (0, 1, 0)),
                       rotate(self.phi, (0, 0, 1)))
        self.program['u_model'] = model
        self.program.draw('line_strip')

# 1000x2
N = 1000
data = np.c_[
    np.sin(np.linspace(-10, 10, N)*np.pi),
    np.cos(np.linspace(-10, 10, N)*np.pi),
    np.linspace(-2, 2, N)]
data = data.astype(np.float32)

# plot
c = Canvas(data)
app.run()
