# pylint: disable=invalid-name, unused-argument
""" Probably the simplest vispy example """
from vispy import app, gloo

c = app.Canvas(keys="interactive")


@c.connect
def on_draw(event):
    """a callback function called when the canvas needs to be refreshed"""
    gloo.set_clear_color((0.2, 0.4, 0.6, 1.0))
    gloo.clear()


c.show()
app.run()
