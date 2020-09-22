# 04-Tetrahedron

## 1. Introduction

Now, let's go 3D in opengl.

![projection.png](figs/projection.png)

*(figure is copied from the [glumpy](http://glumpy.readthedocs.org/) project)*

In real world, we are facing a LCD which is basically a 2D plane (well, **VR** technology might be a revolution to this), the 3D scene is projected on the plane to create a fake 3D view. We need to understand 3 types of matrix:

 - **Model matrix** maps from an object’s *local coordinate space* into *world space*. For example, a model is described using its local coordinates, and then we may apply model matrix to rotate, sheer or move this object.
 - **View matrix** maps from *world space* to *camera space*. The camera is placed at `(0, 0, 0)` and looks at `(0, 0, z)`, the later vector is used to generate this view matrix. View matrix serves as place the object orientated at the scene in front of the camera.
 - **Projection matrix** maps from *camera* to *screen space*, i.e., perspective projection or orthographic projection. This matrix mapps 3D world to 2D scene when rendering.

More details on how these matrix was generated can be found at any computer graphic book.

**Note:** the axis (coordinates) of opengl follows right-hand rule, where `+x` is left-to-right, `+y` is down-to-up, and `+z` is the direction of your thumb when you curl the fingers of your right-hand from `+x` to `+y`.

![right-hand](figs/right-hand.png)

Based on previous tutorial, we can write a 3D version shader as,

```python
vertex = """
uniform mat4   u_model;         // Model matrix
uniform mat4   u_view;          // View matrix
uniform mat4   u_projection;    // Projection matrix
uniform vec4   u_color;         // mask color for edge plotting
attribute vec3 a_position;
attribute vec4 a_color;
varying vec4   v_color;

void main()
{
    gl_Position = u_projection * u_view * u_model * vec4(a_position, 1.0);
    v_color = a_color * u_color;
}
"""
```

```python
fragment = """
varying vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}
"""
```

## 2. Step-by-step

### 2.1 structural meshes

In this example, we will rendering a rotating tetrahedron (or pyramid). A tetrahedron consists of 4 vertices and 4 triangles. Traditionally, in order to render 4 triangles, we need to specify 12 vertices. However, this procedure can be simplified by simply providing the **structure** or the **connectivities** of these triangles.

![tetrahedron.png](figs/tetrahedron.png)

For example, the face outwards can be described using `(0, 1, 3)` (**Note:** that the triangles are usually numbered in a counter-clockwise order, this is a MUST for FEM/CFD applications), the edge can be specified as `(3, 2)`, etc.

After building these indicies, we must convert them to `gloo.IndexBuffer` before passing them to `draw`. Triangles indices are used to draw `triangles` or `triangle stripe`, while Edges indices are used to draw the outline of 3D shape.

```python
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
E = np.array([(0, 1), (1, 2), (2, 0), (1, 3), (2, 3), (0, 3)],
             dtype=np.uint32)
# colors of each vertice
C = np.array([(1, 0, 0, 1),
              (0, 1, 0, 1),
              (0, 0, 1, 1),
              (1, 1, 0, 1)], dtype=np.float32)
```

where `V` is the positions for vertices, `I` is the connectivity of triangles, `C` is colors for vertices, `E` is the edges.

**Note:** `I` and `E` must be converted to `IndexBuffer` using,
```python
self.I = gloo.IndexBuffer(I)
self.E = gloo.IndexBuffer(E)
```

`V` and `C` can be binded using traditional methods, `I` and `E` are passed to `draw` during rendering.

### 2.2 the transformation matrix

The transformation matrices can be generated using
```python
from vispy.util.transforms import translate, perspective, rotate
```

 - `u_model`, a `mat4` matrix, can be rotate, sheer, move, etc., which is generated using `rotate` in this example,
 - `u_view`, a `mat4` matrix, change the world space to camera space,
 - `u_projection`, a `mat4` matrix, from the camera to the screen.

The functions are,

 - `rotate(angle, axis)` rotates a angle (in degrees) centered at axis (vector),
 - `translate(offset)` places the camera,
 - `perspective(fovy, aspect, znear, zfar)` performs the perspective projection.

For example,
```python
self.program['u_model'] = rotate(30, (0, 0, 1))
self.program['u_view'] = translate((0, 0, -5))
self.program['u_projection'] = perspective(45.0, ratio, 2.0, 10.0)
```

**Note:** about composite transformation.

Multiplying composite transformation matrices is at the core of all
modern graphics libraries. In `GDI+`, composite transformations are built from left to right. If S, R, and T are scale, rotation, and translation matrices respectively, then the product SRT (in that order) is the matrix of the composite transformation that first scales, then rotates, then translates. The matrix produced by the product SRT is different from the matrix produced by the product TRS.

### 2.3 (important) the order of composite transformations

Take rotation for example. Two rotations can be combined as one be pre-multiplication of these two matrices,

```python
a = rotate(theta, (0, 1, 0))
b = rotate(phi, (0, 0, 1))
c = np.dot(a, b)
```

If we use `c` as the `model` transformation matrix, then it will be applied on vertices via firstly rotate `theta` degrees around `(0, 1, 0)` and then `phi` degrees around `(0, 0, 1)`. Pretty counter-intuitive ?

**Explaination:**

The reason behind this is that (see in tutorial `02-shaders`), **Python is row-major** while ** OpenGL is column major**. In `vispy.util.transforms`, the function `rotate` transpose the output of the generating matrix (*see the code*). So the matrix `c` sent to the shader is actually `(a.Tb.T)` or `(ba).T` rather than `(ab)`. Henceforth, when multiply a vertex using `cv`, the rotation `a` will be applied first and then `b` ! Remember this convention (although it caused me a lot of confusions), as `vispy` may not change this (or need to) in future.

**References:**

 1. **best:** [Confusion between C++ and OpenGL matrix order (row-major vs column-major)](http://stackoverflow.com/questions/17717600/confusion-between-c-and-opengl-matrix-order-row-major-vs-column-major)
 2. **vispy:** [Vispy issue 507](https://github.com/vispy/vispy/issues/507)
 3. **discussions:** [Column Vectors Vs. Row Vectors](http://steve.hollasch.net/cgindex/math/matrix/column-vec.html)
 4. [Prototyping OpenGL applications with PyOpenGL](http://www.siafoo.net/article/58)

### 2.4 config OpenGL using `vispy.gloo`

In `gloo.set_state`, it controls many behaviors of OpenGL, to name a few:

 - `presets`, could be `'opaque'`, `'translucent'`, `'additive'`. See `gloo.wrappers.py` for more details. These values preset the following values to their default.
 - `blend`. (**important**) Blending can be used to make objects appear **transparent**. However, blending alone is not enough. There are a number of steps that you must take to make transparency work.
 - `depth_test`. (**important**) The Depth Test is a per-sample processing operation performed after the Fragment Shader (and sometimes before). The Fragment's output depth value may be tested against the depth of the sample being written to. If the test fails, the fragment is discarded. If the test passes, the depth buffer will be updated with the fragment's output depth, unless a subsequent per-sample operation prevents it (such as turning off depth writes).
 - `cull_face`. Face culling allows non-visible triangles of closed surfaces to be culled before expensive Rasterization and Fragment Shader operations. To activate face culling, `GL_CULL_FACE` must first be enabled with `glEnable`. By default, face culling is disabled.
 - `polygon_offset_fill`. (**important**) Specifies a scale factor that is used to create a variable depth offset for each polygon. Each fragment's depth value will be offset after it is interpolated from the depth values of the appropriate vertices. The value of the offset is `factor × DZ + r × units`, where DZ is a measurement of the change in depth relative to the screen area of the polygon, and r is the smallest value that is guaranteed to produce a resolvable offset for a given implementation. To achieve a nice rendering of the highlighted solid object without visual artifacts, you can either add a positive offset to the solid object (push it away from you) or a negative offset to the wireframe (pull it towards you).

In this demo, we let,
```python
# config and set viewport
gloo.set_viewport(0, 0, *self.physical_size)
gloo.set_clear_color('white')
gloo.set_state('translucent')
gloo.set_polygon_offset(1.0, 1.0)
```

**References:**

 1. About `polygon_offset`. [Meaning and usage of the factor parameter in glPolygonOffset](http://stackoverflow.com/questions/13431174/meaning-and-usage-of-the-factor-parameter-in-glpolygonoffset)
 2. About the parameters of OpenGL. [Chapter 6. Blending, Antialiasing, Fog, and Polygon Offset](http://www.glprogramming.com/red/chapter06.html). **Read the red book on opengl.**

**Note:** there is no 100% safe transparency solution, you may refer to,

 1. **Depth Peeling**, [Order Independent Transparency with Dual Depth Peeling](http://developer.download.nvidia.com/SDK/10/opengl/src/dual_depth_peeling/doc/DualDepthPeeling.pdf)
 2. OpenGL subscribe, [Order Independent Transparency](http://www.openglsuperbible.com/2013/08/20/is-order-independent-transparency-really-necessary/)
 3. Vispy issue 1076, [cutting volume data](https://github.com/vispy/vispy/issues/1076)
 4. **Vispy Wiki**, [Tech. Transparency](https://github.com/vispy/vispy/wiki/Tech.-Transparency)

### 2.5 run the demo

Then, the tetrahedron can be drawed as (we need 100% transparent tetrahedron, so `depth_test` is disabled),
```python
gloo.set_state(blend=True, depth_test=False, polygon_offset_fill=True)
self.program['u_color'] = [1.0, 1.0, 1.0, 1.0]
self.program.draw('triangles', self.I)
```

The lines (edges) can be drawed as (the lines need not to be transparent, so we disable `blend`),
```python
gloo.set_state(blend=False, depth_test=False, polygon_offset_fill=True)
self.program['u_color'] = [0.0, 0.0, 0.0, 1.0]
self.program.draw('triangles', self.E)
```

## 3. Code

[04-tetrahedron.py](examples/04-tetrahedron.py)

## 4. Exercises

You may modify `blend`, `depth_test`, `polygon_offset_fill`, `cull_face` to the demo, see what is their functions.

