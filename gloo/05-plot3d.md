# 05-plot3d

## 1. Introduction

In this example, we will extend our previous `plot` command to `plot3d`. This tutorial is a straghtforward extension to `04-tetrahedron`, except that we enable the 3D rendering capability.

In this tutorial, we will also learn how to tweak the look and feel of your plots, add customized commands such as `line_width` or line styles, we will also show how to add points (scatter plot) and modify the way scatter points render.

We do not need to build the `IndexBuffers`, all we need in `plot3d` is providing the `(x, y, z)` and using `draw(line_strip)`.

The three matrix, `perspective`, `view` and `model` needs to be changed accordingly. For example, `perspective` needs to be changed every time the canvas is resized,

```python
ratio = event.physical_size[0] / float(event.physical_size[1])
self.program['u_projection'] = perspective(45.0, ratio, 2.0, 10.0)
```

The `view` and `model` need to be modified according to the views, for example, the parameter `z` controls the zoom of the plot, `theta` and `phi` rotate the plot around y-axis and z-axis respectively,

```python
view = translate((0, 0, -self.z))
model = np.dot(rotate(self.theta, (0, 1, 0)),
               rotate(self.phi, (0, 0, 1)))
```

## 2. Customize your plot

### 2.1 Toggle line width

There is a OpenGL attributes called `glLineWidth`, search in `gloo.wrapper`, you will find,

```python
# config your lines
gloo.set_line_width(1.25)
```

### 2.2 Antialiasing

### 2.3 Markers

## 3. Code

[02-plot3d.py](examples/02-plot3d.py)

## 4. Exercises

