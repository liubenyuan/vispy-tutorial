# 01-basic

## 1. Introduction

We will create a bare minimal window using gloo. This example is copied from the main `vispy` repository.

[Getting started with Vispy](http://ipython-books.github.io/featured-06/) is a good way to start!

## 2. The code

[01-basic.py](example/01-basic.py)

## 3. Step-by-step

 1. import
```
from vispy import app, gloo
```
 2. create a canvas using `app.Canvas()`
 3. connect to event `@c.connect`, modify `on_draw(event)` to do somthing each time the canvas needs to be refreshed.
 4. run your demo using
```
c.show()
app.run()
```

## 4. Note