# 02-shaders

Nice tutorial [Modern OpenGL tutorial (python)](http://www.labri.fr/perso/nrougier/teaching/opengl/)

## 1. Introduction

### 1.1 Shaders

![gl-pipeline.png](figs/gl-pipeline.png)

(figures copied from [glumpy.github.io](https://glumpy.github.io/_images/gl-pipeline.png))

Shaders are pieces of program (using a C-like language) that are build onto the GPU and executed during the rendering pipeline.

(text copied from [Modern OpenGL tutorial (python)](http://www.labri.fr/perso/nrougier/teaching/opengl/))

To program shaders, we needs to write two programs,

 - `vertex`: It outputs the position of a vertex, `gl_Position`, Which is basically a 4-tuple, for example `vec4(x, y, z, t)`. If you are going to program only in 2D, then `z` may be ommited. `t` is always set to `1.0`.
 - `fragment`: It outputs the color of the fragment, `gl_FragColor`, which is also a 4-tuple, with `vec4(r, g, b, a)`. `a` controls the alpha of this fragment.

### 1.2 Data Types of GLSL

`vec4` is a special data type for GLSL (The OpenGL Shading Language). Some basic data types are (see [Data Type of GLSL](https://www.opengl.org/wiki/Data_Type_(GLSL))):

 - `bool`, `int`, `uint`, `float`: typical data types for C.
 - `vecn`: a vector of single-precision floating-point numbers, where `n` could be 2, 3, 4.
 - `matn`: A matrix with n columns and n rows. Shorthand for matnxn
 - `matnxm`: A matrix with n columns and m rows. OpenGL uses column-major matrices, which is standard for mathematics users. Example: mat3x4.

**Note:** GLSL stores data in a colume-first order.

### 1.3 Attributes, Uniforms And Varyings

There are three types of inputs and outputs in a shader: uniforms, attributes and varyings.

(text copied and modified from [GLSL: An Introduction](http://nehe.gamedev.net/article/glsl_an_introduction/25007/))

 - `attribute` : Attributes are **only available in vertex** shader and they are input values which change every vertex, for example the vertex position or normals. Attributes are **read-only**.
 - `uniform` : values which do not change during a rendering, for example the light position or the light color. Uniforms are available in **both vertex and fragment** shaders. Uniforms are **read-only**.
 - `varying` : Varyings are used for passing data from a vertex shader to a fragment shader. Varyings are (perspective correct) interpolated across the primitive. Varyings are **read-only in fragment** shader but are **read and writeable in vertex** shader (but be careful, reading a varying type before writing to it will return an undefined value). If you want to use varyings you have to **declare the same varying** in your vertex shader and in your fragment shader.

### 1.4 Built-in types

**built-in attributes:**

 - `gl_Vertex` : 4D vector representing the vertex position
 - `gl_Normal` : 3D vector representing the vertex normal
 - `gl_Color` : 4D vector representing the vertex color
 - `gl_MultiTexCoordX` : 4D vector representing the texture coordinate of texture unit X

**built-in uniforms:**

 - `gl_ModelViewMatrix` : 4x4 Matrix representing the model-view matrix.
 - `gl_ModelViewProjectionMatrix` : 4x4 Matrix representing the model-view-projection matrix.
 - `gl_NormalMatrix` : 3x3 Matrix representing the inverse transpose model-view matrix. This matrix is used for normal transformation.

**GLSL Built-In Varyings:**

 - `gl_FrontColor` : 4D vector representing the primitives front color
 - `gl_BackColor` : 4D vector representing the primitives back color
 - `gl_TexCoord[X]` : 4D vector representing the Xth texture coordinate

### 1.5 Outputs of shaders

There are some built-in types which are used for shader output:
 - `gl_Position` : 4D vector (`vec4`) representing the final processed vertex position. Only available in vertex shader.
 - `gl_FragColor` : 4D vector (`vec4`) representing the final color which is written in the frame buffer. Only available in fragment shader.
 - `gl_FragDepth` : float (`float`) representing the depth which is written in the depth buffer. Only available in fragment shader.

### 1.6 The language (GLSL)

 - GLSL is 100% type safe. You are not allowed to assign an integer to a float without casting (by constructor):
```
float my_float = 1;         // Wont Work! 1 Is An Integer!
float my_new_float = 1.0;   // Will Work!
```
 - Casts have to be done using constructors. For example this wont work:
```
my_vec2 = (vec2)my_int_vec;  // Wont Work Because No Constructor Is Used!
my_vec2 = vec2(my_int_vec);  // Will Work!
```
 - Vectors and matrices can be only be filled with user-data using constructors:
```
vec3 my_vec = vec3(1.0, 1.0, 1.0);
mat3 my_mat = mat3(1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0);
```
 - Vector multiplication is component-wise:
```
vec3 my_vec1 = vec3(5.0, 1.0, 0.0);
vec3 my_vec2 = vec3(1.0, 3.0, 4.0);
vec3 product = my_vec1 * my_vec2;  // Will Return This Vector: (5.0, 3.0, 0.0)
```
 - Vector with matrix multiplication is also available.
   - `mat * vec` will treat the vector as a column-vector (OpenGL standard)
   - `vec * mat` will treat the vector as a row-vector (DirectX standard)

 - There are also many built-in function which can (and should) be used:
   - `dot` : a simple dot product
   - `cross` : a simple cross product

## 2. Code

## 3. Step-by-step

## 4. Note
