# pylint: disable=invalid-name, no-member, unused-argument
""" passing varyings to fragment """
import numpy as np
from vispy import app, gloo
from vispy.util.transforms import translate, perspective, rotate

# note the 'color' and 'v_color' in vertex
vertex = """
uniform mat4   u_model;         // Model matrix
uniform mat4   u_view;          // View matrix
uniform mat4   u_projection;    // Projection matrix
uniform vec4   u_color;
attribute vec3 a_position;
attribute vec4 a_color;
varying vec4   v_color;

void main()
{
    gl_Position = u_projection * u_view * u_model * vec4(a_position, 1.0);
    v_color = a_color*u_color;
}
"""

# note the varying 'v_color', it must has the same name as in the vertex.
fragment = """
varying vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}
"""


class Canvas(app.Canvas):
    """ build canvas class for this demo """

    def __init__(self):
        app.Canvas.__init__(self, size=(512, 512), title='scaling quad',
                            keys='interactive')

        # program with 4 vertices
        tet = gloo.Program(vert=vertex, frag=fragment)

        # bind data
        V = np.array([(0, 0, 0),
                      (1, 0, 0),
                      (1.0/2.0, np.sqrt(3.0)/2.0, 0),
                      (1.0/2.0, np.sqrt(3.0)/6.0, np.sqrt(2.0/3.0))],
                     dtype=np.float32)
        # triangles specified by connecting matrix
        # it can also be initialized using itertools
        I = np.array([(0, 1, 2),
                      (0, 1, 3),
                      (0, 2, 3),
                      (1, 2, 3)], dtype=np.uint32)
        # draw outline
        L = np.array([(0, 1), (1, 2), (2, 0), (1, 3), (2, 3), (0, 3)],
                     dtype=np.uint32)
        # colors of each vertice
        C = np.array([(1, 0, 0, 1),
                      (0, 1, 0, 1),
                      (0, 0, 1, 1),
                      (1, 1, 0, 1)], dtype=np.float32)

        tet['a_position'] = V
        tet['a_color'] = C

        view = np.eye(4, dtype=np.float32)
        model = np.eye(4, dtype=np.float32)
        projection = np.eye(4, dtype=np.float32)

        view = translate((0, 0, -5))
        tet['u_model'] = model
        tet['u_view'] = view
        tet['u_projection'] = projection

        # build
        self.program = tet
        self.I = gloo.IndexBuffer(I)
        self.L = gloo.IndexBuffer(L)

        # config and set viewport
        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.set_clear_color('white')
        gloo.set_state('opaque')

        # bind a timer
        self.timer = app.Timer('auto', self.on_timer)
        self.theta = 0.0
        self.phi = 0.0
        self.timer.start()

        # show the canvas
        self.show()

    def on_resize(self, event):
        """ canvas resize callback """
        ratio = event.physical_size[0] / float(event.physical_size[1])
        self.program['u_projection'] = perspective(45.0, ratio, 2.0, 10.0)
        gloo.set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        """ canvas update callback """
        gloo.clear()
        # Filled cube
        gloo.set_state(blend=False, depth_test=True, polygon_offset_fill=True)
        self.program['u_color'] = [1.0, 1.0, 1.0, 1.0]
        self.program.draw('triangles', self.I)
        # draw outline
        gloo.set_state(blend=False, depth_test=True, polygon_offset_fill=False)
        gloo.set_depth_mask(False)
        self.program['u_color'] = [0.0, 0.0, 0.0, 1.0]
        self.program.draw('lines', self.L)
        gloo.set_depth_mask(True)

    def on_timer(self, event):
        """ canvas time-out callback """
        self.theta += .5
        self.phi += .5
        self.model = np.dot(rotate(self.theta, (0, 1, 0)),
                            rotate(self.phi, (0, 0, 1)))
        self.program['u_model'] = self.model
        self.update()

# Finally, we show the canvas and we run the application.
c = Canvas()
app.run()
