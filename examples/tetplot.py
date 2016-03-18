# coding: utf-8
# pylint: disable=no-member
""" plot function based on vispy for tetrahedral plots """
from __future__ import absolute_import

from itertools import combinations
import numpy as np
from vispy import app, gloo, visuals, scene


# build vertex shader for tetplot
vertex_shader = """
uniform vec4 u_color;
attribute vec4 a_color;
varying vec4 v_color;

void main()
{
    vec4 visual_pos = vec4($position, 1);
    vec4 doc_pos = $visual_to_doc(visual_pos);
    gl_Position = $doc_to_render(doc_pos);

    v_color = a_color * u_color;
}
"""

# build fragment shader for tetplot
fragment_shader = """
varying vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}
"""


def sim_conv(simplices, N=3):
    """ simplices to any dimension """
    v = [list(combinations(sim, N)) for sim in simplices]
    # change to (num_of_points x N)
    t = np.sort(np.array(v).reshape(-1, N), axis=1)
    # delete duplicated entries
    t_unique = np.unique(t.view([('', t.dtype)]*N)).view(np.uint32)
    return t_unique


def sim2tri(simplices):
    """ convert simplices of high dimension to indices of triangles """
    return sim_conv(simplices, 3)


def sim2edge(simplices):
    """ convert simplices of high dimension to indices of edges """
    return sim_conv(simplices, 2)


# now build our visuals
class TetFaceVisual(visuals.Visual):
    """ template """

    def __init__(self, points, simplices):
        """ plot 3D

        Parameters
        ----------
        points : NDArray of float32
            N x 3 points coordinates
        simplices : NDArray of uint32
            N x 4 connectivity matrix

        """
        visuals.Visual.__init__(self, vertex_shader, fragment_shader)

        # build Vertices buffer
        self.V = gloo.VertexBuffer(points)

        # build index buffer
        I = sim2tri(simplices)
        self.I = gloo.IndexBuffer(I)

        # bind data
        self.shared_program.vert['position'] = self.V
        self._index_buffer = self.I

        # config color
        self.shared_program['u_color'] = (1.0, 1.0, 1.0, 1.0)
        self.shared_program['a_color'] = np.ones((points.shape[0], 4),
                                                 dtype=np.float32)

        # config
        self.set_gl_state('translucent',
                          blend=True,
                          depth_test=False,
                          polygon_offset_fill=True,
                          clear_color=(1, 1, 1, 1))
        self._draw_mode = 'triangles'

    def _prepare_transforms(self, view):
        """ This method is called when the user or the scenegraph has assigned
        new transforms to this visual """
        # Note we use the "additive" GL blending settings so that we do not
        # have to sort the mesh triangles back-to-front before each draw.
        tr = view.transforms
        view_vert = view.view_program.vert
        view_vert['visual_to_doc'] = tr.get_transform('visual', 'document')
        view_vert['doc_to_render'] = tr.get_transform('document', 'render')


# now build our visuals
class TetLineVisual(visuals.Visual):
    """ template """

    def __init__(self, points, simplices):
        """ plot tetrahedron edges """
        visuals.Visual.__init__(self, vertex_shader, fragment_shader)

        # build Vertices buffer
        self.V = gloo.VertexBuffer(points)

        # build index buffer
        E = sim2edge(simplices)
        self.E = gloo.IndexBuffer(E)

        # bind data
        self.shared_program.vert['position'] = self.V
        self._index_buffer = self.E

        # config color
        self.shared_program['u_color'] = (0.0, 0.0, 0.0, 1.0)
        self.shared_program['a_color'] = np.ones((points.shape[0], 4),
                                                 dtype=np.float32)

        # config
        self.set_gl_state('opaque',
                          blend=True,
                          depth_test=False,
                          polygon_offset_fill=False,
                          clear_color=(1, 1, 1, 1))
        self._draw_mode = 'lines'

    def _prepare_transforms(self, view):
        """ This method is called when the user or the scenegraph has assigned
        new transforms to this visual """
        # Note we use the "additive" GL blending settings so that we do not
        # have to sort the mesh triangles back-to-front before each draw.
        tr = view.transforms
        view_vert = view.view_program.vert
        view_vert['visual_to_doc'] = tr.get_transform('visual', 'document')
        view_vert['doc_to_render'] = tr.get_transform('document', 'render')


# now build our visuals
class TetPlotVisual(visuals.CompoundVisual):
    """ compound pcolor and plot """

    def __init__(self, points, simplices):
        self._faces = TetFaceVisual(points, simplices)
        self._lines = TetLineVisual(points, simplices)
        visuals.CompoundVisual.__init__(self, [self._faces, self._lines])

    def set_data(self):
        pass


# build your visuals, that's all
TetPlot = scene.visuals.create_visual_node(TetPlotVisual)

# The real-things : plot using scene
# build canvas
canvas = scene.SceneCanvas(keys='interactive', show=True)

# Add a ViewBox to let the user zoom/rotate
view = canvas.central_widget.add_view()
view.camera = 'turntable'
view.camera.fov = 50
view.camera.distance = 5

# data
pts = np.array([(0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
                (1.0, 1.0, 1.0)], dtype=np.float32)

sim = np.array([(0, 1, 2, 3),
                (1, 3, 2, 4)], dtype=np.uint32)

# plot ! note the parent parameter
p1 = TetPlot(pts, sim, parent=view.scene)

# run
app.run()
