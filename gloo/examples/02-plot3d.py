# pylint: disable=invalid-name, no-member, unused-argument
""" basic 3D points plot """

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
    """ build canvas """

    def __init__(self, data, theta=30.0, phi=90.0, z=6.0):
        """ initialize data for plotting

        Parameters
        ----------
        data : array_like
            3D data, Nx3
        theta : float
            rotation around y axis
        phi : float
            rotation around z axis
        z : float
            view depth

        """
        app.Canvas.__init__(self, size=(800, 400), title='plot3d',
                            keys='interactive')

        # build shader program
        program = gloo.Program(vert=vertex, frag=fragment)

        # initialize 3D view
        view = np.eye(4, dtype=np.float32)
        model = np.eye(4, dtype=np.float32)
        projection = np.eye(4, dtype=np.float32)

        view = translate((0, 0, -z))
        program['u_model'] = model
        program['u_view'] = view
        program['u_projection'] = projection
        program['a_position'] = data

        # bind
        self.program = program
        self.theta = theta
        self.phi = phi

        # config
        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.set_clear_color('white')
        gloo.set_state('translucent')

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
        """ refresh canvas """
        gloo.clear()
        model = np.dot(rotate(self.theta, (0, 1, 0)),
                       rotate(self.phi, (0, 0, 1)))
        # note the convention is, theta is applied first and then phi
        # see vispy.utils.transforms,
        # python is row-major and opengl is column major,
        # so the rotate function transposes the output.
        self.program['u_model'] = model
        self.program.draw('line_strip')

# 1000x3
N = 1000
data3d = np.c_[
    np.sin(np.linspace(-10, 10, N)*np.pi),
    np.cos(np.linspace(-10, 10, N)*np.pi),
    np.linspace(-2, 2, N)]
data3d = data3d.astype(np.float32)

# plot
c = Canvas(data3d)
app.run()
