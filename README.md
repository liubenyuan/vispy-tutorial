# vispy tutorial

*tutorials about vispy*

## About

`vispy` is a high performance 2D/3D visualization library. It provides low-level and high-level interfaces that levage the power of GPU for high performance plotting.

### How to install `vispy`

Install globally

```
$ cd /path/to/vispy
$ python setup.py install
```

Install locally (recommended for using cutting-edge features of `vispy`)

```
export PYTHONPATH=/path/to/vispy/vispy
```

## Introduction

This tutorial focus on two main blocks of `vispy`:

 - `gloo` : low-level OpenGL interfaces
 - `plot` : high-level programming interface

The purposes:

 - learning how to tweak low-level `gloo`, customizing plot functions, especially for `triangle` or `tetrahedron` unstructure meshes.
 - learning how to use high-level `plot` to generate or export publication ready figures

## References

 - Official website : [vispy.org](http://vispy.org/)
 - [Modern OpenGL tutorial (python)](http://www.labri.fr/perso/nrougier/teaching/opengl/) by Nicolas P. Rougier
 - [Getting started with Vispy](http://ipython-books.github.io/featured-06/) by Cyrille Rossant
