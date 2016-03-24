""" port oit, copied from glumpy """
import numpy as np

from vispy import app, gloo
from vispy.gloo import gl
from vispy.util.transforms import translate, perspective, rotate

vert_quads = """
uniform mat4 u_model;         // Model matrix
uniform mat4 u_view;          // View matrix
uniform mat4 u_projection;    // Projection matrix

attribute vec4 a_color;
attribute vec3 a_position;

varying vec4 v_color;
varying float v_depth;
varying float v_pass;

void main()
{
    gl_Position = u_projection * u_view * u_model * vec4(a_position, 1.0);
    v_depth = -(u_view * u_model * vec4(a_position, 1.0)).z;
    v_color = a_color;
}
"""

frag_quads = """
uniform float u_pass;    // 2-pass

varying vec4 v_color;
varying float v_depth;

void main()
{
    float z = v_depth;
    float alpha = v_color.a;
    float weight = pow(alpha + 0.01f, 2.0f) *
                   clamp(0.3f/(1e-5f + pow(abs(z)/200.0f, 4.0f)), 1e-2f, 3e3f);

    if( u_pass < 0.5 )
        gl_FragData[0] = vec4(v_color.rgb * weight, alpha) ;
    else
        gl_FragData[0] = vec4(alpha * weight);
}
"""

vert_post = """
attribute vec2 a_position;
varying vec2 v_texcoord;

void main(void)
{
    gl_Position = vec4(a_position, 0, 1);
    v_texcoord = (a_position + 1.0)/2.0;
}
"""

frag_post = """
uniform sampler2D tex_accumulation;
uniform sampler2D tex_revealage;

varying vec2 v_texcoord;

void main(void)
{
    vec4 accum = texture2D(tex_accumulation, v_texcoord);
    float r = accum.a;
    accum.a = texture2D(tex_revealage, v_texcoord).r;
    if (r >= 1.0)
        discard;
    gl_FragColor = vec4(accum.rgb / clamp(accum.a, 1e-4, 5e4), r);
}
"""

C0 = (0.75, 0.75, 0.75, 1.00)
C1 = (1.00, 0.00, 0.00, 0.25)
C2 = (1.00, 1.00, 0.00, 0.25)
C3 = (0.00, 0.00, 1.00, 0.25)


class Canvas(app.Canvas):
    """ build canvas class for this demo """

    def __init__(self):
        """ initialize the canvas """
        app.Canvas.__init__(self,
                            size=(512, 512),
                            title='scaling quad',
                            keys='interactive')

        # RGBA32F float texture size[0]=height, size[1]=width
        a = np.zeros((self.size[0], self.size[1], 4), np.float32)
        accum_texture = gloo.Texture2D(a)

        # R32F float texture
        b = np.zeros((self.size[0], self.size[1]), np.float32)
        reveal_texture = gloo.Texture2D(b)

        self.accum = accum_texture
        self.reveal = reveal_texture

        # Framebuffer with two color targets
        framebuffer = gloo.FrameBuffer(color=self.accum)
        self.framebuffer = framebuffer

        #
        quads = gloo.Program(vert_quads, frag_quads, count=12)
        pos = [(-1, -1, -1), (-1, +1, -1), (+1, -1, -1), (+1, +1, -1),
               (-1, -1, 0), (-1, +1, 0), (+1, -1, 0), (+1, +1, 0),
               (-1, -1, +1), (-1, +1, +1), (+1, -1, +1), (+1, +1, +1)]
        quads["a_position"] = np.array(pos) * 10

        quads["a_color"] = C1, C1, C1, C1, C2, C2, C2, C2, C3, C3, C3, C3
        quads['u_pass'] = 0
        indices = np.zeros((3, 6), dtype=np.uint32)
        indices[0] = 0 + np.array([0, 1, 2, 1, 2, 3])
        indices[1] = 4 + np.array([0, 1, 2, 1, 2, 3])
        indices[2] = 8 + np.array([0, 1, 2, 1, 2, 3])
        indices = gloo.IndexBuffer(indices)
        self.indices = indices

        # Post composition
        post = gloo.Program(vert_post, frag_post)
        post['tex_accumulation'] = self.accum
        post['tex_revealage'] = self.reveal
        post['a_position'] = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # intialize transformation matrix
        view = np.eye(4, dtype=np.float32)
        model = np.eye(4, dtype=np.float32)
        projection = np.eye(4, dtype=np.float32)

        # set view
        view = translate((0, 0, -40))

        # set rotate
        theta = 30
        phi = -45
        model = np.dot(rotate(theta, (0, 0, 1)),
                       rotate(phi, (1, 0, 0)))

        # projection
        projection = perspective(50.0, 1.0, 0.1, 100.0)

        # assign
        quads['u_model'] = model
        quads['u_view'] = view
        quads['u_projection'] = projection

        #
        self.quads = quads
        self.post = post

        # config and set viewport
        gloo.set_viewport(0, 0, *self.physical_size)
        # gloo.set_polygon_offset(1.0, 1.0)

        # show the canvas
        self.show()

    def on_resize(self, event):
        """ canvas resize callback """
        gloo.set_viewport(0, 0, *event.physical_size)
        # ratio = event.physical_size[0] / float(event.physical_size[1])
        # self.quads['u_projection'] = perspective(50.0, ratio, 0.1, 100.0)

    def on_draw(self, event):
        """ canvas update callback """

        # Clear depth and color buffers
        gloo.clear(color=C0)

        # Filled cube
        gloo.set_state(depth_test=True, blend=True, depth_mask=False)
        #gloo.set_depth_mask(False)
        #gl.glEnable(gl.GL_DEPTH_TEST)
        #gl.glDepthMask(gl.GL_FALSE)
        #gl.glEnable(gl.GL_BLEND)

        #
        self.quads['u_pass'] = 0.0
        self.framebuffer.color_buffer = self.accum
        self.framebuffer.activate()
        gloo.clear(color=(0, 0, 0, 0))
        #gloo.set_blend_func('one', 'one')
        #gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE)
        gl.glBlendFuncSeparate(gl.GL_ONE, gl.GL_ONE,
                               gl.GL_ONE, gl.GL_ONE)
        self.quads.draw('triangles', self.indices)
        self.framebuffer.deactivate()

        #
        self.quads['u_pass'] = 1.0
        self.framebuffer.color_buffer = self.reveal
        self.framebuffer.activate()
        gloo.clear(color=(1, 1, 1, 1))
        #gloo.set_blend_func('zero', 'one_minus_src_color')
        #gl.glBlendFunc(gl.GL_ZERO, gl.GL_ONE_MINUS_SRC_COLOR)
        gl.glBlendFuncSeparate(gl.GL_ZERO, gl.GL_ONE_MINUS_SRC_COLOR,
                               gl.GL_ZERO, gl.GL_ONE_MINUS_SRC_COLOR)
        self.quads.draw('triangles', self.indices)
        self.framebuffer.deactivate()

        # Filled cube
        #gloo.set_blend_func('src_alpha', 'one_minus_src_alpha')
        gl.glBlendFuncSeparate(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA,
                               gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        # gloo.set_state('translucent', blend=True, depth_test=False)
        self.post.draw('triangle_strip', self.indices)

# Finally, we show the canvas and we run the application.
c = Canvas()
app.run()
