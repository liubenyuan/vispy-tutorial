# 02-shaders

## 1. Introduction

### 1.1 Shaders

The GLSL code of `vispy.gloo` is built on top of two shaders : `vertex` shader and `fragment` shader.

![gl-pipeline.png](figs/gl-pipeline.png)

*(figures copied from [glumpy.github.io](https://glumpy.github.io/_images/gl-pipeline.png))*

Shaders are pieces of program (using a C-like language) that are build onto the GPU and executed during the rendering pipeline.
The vertex shader is executed for each vertex that is given to the rendering pipeline (we’ll see what does that mean exactly later) and the fragment shader is executed on each fragment that is generated after the vertex stage.

*(text copied from [Modern OpenGL tutorial (python)](http://www.labri.fr/perso/nrougier/teaching/opengl/))*

To program shaders, we needs to write two programs,

 1. `vertex`: It outputs the position of a vertex, `gl_Position`, Which is basically a 4-tuple, for example `vec4(x, y, z, w)`. If you are going to program only in 2D, then `z` may be ommited.
 2. `fragment`: It outputs the color of the fragment, `gl_FragColor`, which is also a 4-tuple, with `vec4(r, g, b, a)`. `rgb` represents the color palette, `a` controls the alpha of this fragment.

**Note:** W is the fourth coordinate of a three dimensional vertex; This vertex is called homogeneous vertex coordinate. **It can be treated as a scaling parameter for matrix transformations**. In few words, the W component is a factor which divide the other vector components. When W is 1.0, the homogeneous vertex coordinates are "normalized". To compare two vertices, you should normalize the W value to 1.0.

**Note:** A typical projection does `w_out = -z_in`. That's why people sometimes call this the **perspective divide**.

 - Think to the vertex (1,1,1,1). Now increase the W value (w > 1.0). The normalized position is **scaling!** and it is going to the origin.
 - Think to the vertex (1,1,1,1). Now decrease the W value (W < 1.0). The normalized position is going to an infinite point.
 - If W is exactly 0, the vector does not behave as a **position** but as a **direction** (think directional light); i.e., it represents all the lines parallel to a given line.

### 1.2 Data types of GLSL

`vec4` is a special data type for GLSL (The OpenGL Shading Language). In GLSL, some other basic data types are (see [Data Type of GLSL](https://www.opengl.org/wiki/Data_Type_(GLSL)):

 - `bool`, `int`, `uint`, `float`: typical data types for C.
 - `vecn`: a vector of single-precision floating-point numbers, where `n` could be 2, 3, 4.
 - `matn`: A matrix with n columns and n rows, shorthand for matnxn
 - `matnxm`: A matrix with n columns and m rows. OpenGL uses **column-major** matrices, which is standard for mathematics users. Example: mat3x4.

**Note:** GLSL stores data in colume first order.

### 1.3 Attributes, uniforms and varyings

There are three types of inputs and outputs in a shader: attributes, uniforms and varyings.

*(text copied and modified from [GLSL: An Introduction](http://nehe.gamedev.net/article/glsl_an_introduction/25007/))*

 - `attribute` : attributes are **only available in vertex** shader and they are input values which change every vertex, for example the vertex position or normals. Attributes are **read-only**.
 - `uniform` : values which do not change during a rendering, for example the light position or the light color. Uniforms are available in **both vertex and fragment** shaders. Uniforms are **read-only** from shaders.
 - `varying` : varyings are used for passing data from a vertex shader to a fragment shader. Varyings are (perspective correct) interpolated across the primitive. Varyings are **read-only in fragment** shader but are **read and writeable in vertex** shader (but be careful, reading a varying type before writing to it will return an undefined value). If you want to use varyings you have to **declare the same varying** in your vertex shader and in your fragment shader.

### 1.4 Built-in types

**1.4.1 built-in attributes:**

 - `gl_Vertex` : 4D vector representing the vertex position
 - `gl_Normal` : 3D vector representing the vertex normal
 - `gl_Color` : 4D vector representing the vertex color
 - `gl_MultiTexCoordX` : 4D vector representing the texture coordinate of texture unit X

**1.4.2 built-in uniforms:**

 - `gl_ModelViewMatrix` : 4x4 Matrix representing the model-view matrix.
 - `gl_ModelViewProjectionMatrix` : 4x4 Matrix representing the model-view-projection matrix.
 - `gl_NormalMatrix` : 3x3 Matrix representing the inverse transpose model-view matrix. This matrix is used for normal transformation.

**1.4.3 built-in varyings:**

 - `gl_FrontColor` : 4D vector representing the primitives front color
 - `gl_BackColor` : 4D vector representing the primitives back color
 - `gl_TexCoord[X]` : 4D vector representing the Xth texture coordinate

### 1.5 Outputs of shaders

There are some built-in types which are used for shader output (which is especially important in `vispy.gloo`):

 - `gl_Position` : 4D vector (`vec4`) representing the final processed vertex position. Only available in **vertex shader**.
 - `gl_FragColor` : 4D vector (`vec4`) representing the final color which is written in the frame buffer. Only available in **fragment shader**.
 - `gl_FragDepth` : float (`float`) representing the depth which is written in the depth buffer. Only available in **fragment shader**.

### 1.6 The language (GLSL)

 - GLSL is 100% type safe. You are not allowed to assign an integer to a float without casting **(by constructor)**:
```
float my_float = 1;         // Wont Work! 1 Is An Integer!
float my_new_float = 1.0;   // Will Work!
```

 - Casts have to be done using **constructors**. For example this wont work:
```
my_vec2 = (vec2)my_int_vec;  // Wont Work Because No Constructor Is Used!
my_vec2 = vec2(my_int_vec);  // Will Work!
```

 - Vectors and matrices can be only be filled with user-data using **constructors**:
```
vec3 my_vec = vec3(1.0, 1.0, 1.0);
mat3 my_mat = mat3(1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0);
```

 - Vector multiplication is **component-wise**:
```
vec3 my_vec1 = vec3(5.0, 1.0, 0.0);
vec3 my_vec2 = vec3(1.0, 3.0, 4.0);
vec3 product = my_vec1 * my_vec2;  // Will Return This Vector: (5.0, 3.0, 0.0)
```

 - Vector with matrix multiplication is also available (**OpenGL uses column-major ordering**, But, **Python uses row-major ordering**!)
   - `mat * vec` will treat the vector as a column-vector (OpenGL standard)
   - `vec * mat` will treat the vector as a row-vector (DirectX standard)

 - There are also many built-in function which can (and should) be used:
   - `dot`: a simple dot product
   - `cross`: a simple cross product

## 2. Step-by-step

Nice tutorial from [Modern OpenGL tutorial (python)](http://www.labri.fr/perso/nrougier/teaching/opengl/)

For example, we are going to plot a 2D data, the `position` of each data point can be specified by a `vec2` **vertex**, and the plot can be rendered using **fragment** with a fixed color.

The vertex can be programmed as,
```python
vertex = """
attribute vec2 a_position;
void main(void)
{
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""
```
where `a_position` is a `vec2` attribute that is used as input for the position of vertex.

The fragment can be programmed as,
```python
fragment = """
void main()
{
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
"""
```

We build the pipeline using `gloo.Program`,
```python
program = gloo.Program(vert=vertex, frag=fragment)
```

2D test data can be conveniently generated using `numpy`,
```python
# generate Nx2 test data
N = 1000
data = np.c_[
    np.linspace(-1, 1, N),
    np.random.uniform(-0.5, +0.5, N)]
```
The `a_position` attibutes can be assigned using,
```python
program['a_position'] = data.astype('float32')
```

**But, how could we draw (render) all the vertex?**

GLSL provides with some basic drawing primitives,

![gl-primitivies](figs/gl-primitives.png)

Here, `line_stripe` can be used for 2D plotting.
```python
@c.connect
def on_draw(event):
    gloo.clear((1, 1, 1, 1))
    program.draw('line_strip')
```

That's all!

## 3. Code

[02-plot.py](examples/02-plot.py)

## 4. Exercise

There are many drawing (rendering) mode in the shaders, as illustrated in the graph. Pick one and modify your code, for example, what would `points` be ? Plot your results and find out why.
