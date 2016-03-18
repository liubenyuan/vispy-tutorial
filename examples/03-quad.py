# pylint: disable=invalid-name, no-member, unused-argument
""" passing varyings to fragment """
import numpy as np
from vispy import app, gloo

# note the 'color' and 'v_color' in vertex
vertex = """
uniform float scale;
attribute vec2 a_position;
attribute vec4 color;
varying vec4 v_color;

void main(void)
{
    gl_Position = vec4(a_position*scale, 0.0, 1.0);
    v_color = color;
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
        program = gloo.Program(vert=vertex, frag=fragment, count=4)

        # bind data
        program['a_position'] = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        program['color'] = [(1, 0, 0, 1),
                            (0, 1, 0, 1),
                            (0, 0, 1, 1),
                            (1, 1, 0, 1)]
        program['scale'] = 1.0
        self.program = program

        # set viewport
        gloo.set_viewport(0, 0, *self.physical_size)

        # bind a timer
        self.timer = app.Timer('auto', self.on_timer)
        self.clock = 0.0
        self.timer.start()

        # show the canvas
        self.show()

    @staticmethod
    def on_resize(event):
        """ canvas resize callback """
        gloo.set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        """ canvas update callback """
        gloo.set_clear_color('white')
        gloo.clear()
        self.program.draw('triangle_strip')

    def on_timer(self, event):
        """ canvas time-out callback """
        self.clock += 0.01 * np.pi
        self.program['scale'] = 0.5 + 0.5 * np.cos(self.clock)
        self.update()

# Finally, we show the canvas and we run the application.
c = Canvas()
app.run()
