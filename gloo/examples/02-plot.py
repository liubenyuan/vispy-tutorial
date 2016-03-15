# learning vispy
# http://ipython-books.github.io/featured-06/

import numpy as np
from vispy import app, gloo

# In order to display a window, we need to create a Canvas.
c = app.Canvas(keys='interactive')

# When using vispy.gloo, we need to write shaders.
# These programs, written in a C-like language called GLSL,
# run on the GPU and give us full flexibility for our visualizations.
# Here, we create a trivial vertex shader that directly displays
# 2D data points (stored in the a_position variable) in the canvas
vertex = """
attribute vec2 a_position;
void main(void)
{
    gl_Position = vec4(a_position, 0.0, 1.0);
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

# Next, we create an OpenGL Program. This object contains the shaders
# and allows us to link the shader variables to Python/NumPy data.
program = gloo.Program(vert=vertex, frag=fragment)

# 1000x2
N = 1000
data = np.c_[
    np.linspace(-1, 1, N),
    np.random.uniform(-0.5, +0.5, N)]
print(data.shape)

# gloo needs 32bit
program['a_position'] = data.astype('float32')


# We create a callback function called when the window is being resized.
# Updating the OpenGL viewport lets us ensure that
# Vispy uses the entire canvas.
@c.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)


# We create a callback function called when the canvas needs to be refreshed.
# This on_draw function renders the entire scene.
@c.connect
def on_draw(event):
    # First, we clear the window in white
    # (it is necessary to do that at every frame)
    gloo.clear((1.0, 1.0, 1.0, 1.0))
    program.draw('line_strip')

# Finally, we show the canvas and we run the application.
c.show()
app.run()
