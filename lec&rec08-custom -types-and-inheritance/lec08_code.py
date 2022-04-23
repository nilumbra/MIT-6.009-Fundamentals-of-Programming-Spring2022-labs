## FRONT MATTER FOR DRAWING/SHOWING IMAGES, ETC
## related to representation from lab 1, but with extra stuff for showing
## images live.  feel free to skip past this to the section labeled SHAPES!

import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


def new_image(width, height, fill=(240, 240, 240)):
    return {
        "height": height,
        "width": width,
        "pixels": [fill for r in range(height) for c in range(width)],
    }


def flat_index(image, x, y):
    return (image["height"] - 1 - y) * image["width"] + x


def get_pixel(image, x, y):
    return image["pixels"][flat_index(image, x, y)]


def set_pixel(image, x, y, c):
    assert isinstance(c, tuple) and len(c) == 3 and all(isinstance(i, int) for i in c)
    if 0 <= x < image["width"] and 0 <= y < image["height"]:
        image["pixels"][flat_index(image, x, y)] = c


def gif_data(im, scale=1):
    out = PILImage.new(mode="RGB", size=(im["width"], im["height"]))
    out.putdata(im["pixels"])
    out = out.resize(
        (int(im["width"] * scale), int(im["height"] * scale)), PILImage.Resampling.NEAREST
    )

    buf = BytesIO()
    out.save(buf, "GIF")
    out.close()
    return base64.b64encode(buf.getvalue())


def show_image(im, scale=1):
    toplevel = tk_root
    # highlightthickness=0 is a hack to prevent the window's own resizing
    # from triggering another resize event (infinite resize loop).  see
    # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
    canvas = tkinter.Canvas(
        toplevel,
        height=im["height"] * scale,
        width=im["width"] * scale,
        highlightthickness=0,
    )
    canvas.pack()
    canvas.img = tkinter.PhotoImage(data=gif_data(im, scale=scale))
    canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)

    def on_resize(event):
        # handle resizing the image when the window is resized
        # the procedure is:
        #  * convert to a PIL image
        #  * resize that image
        #  * grab the base64-encoded GIF data from the resized image
        #  * put that in a tkinter label
        #  * show that image on the canvas
        new_img = PILImage.new(mode="RGB", size=(im["width"], im["height"]))
        new_img.putdata(im["pixels"])
        new_img = new_img.resize((event.width, event.height), PILImage.Resampling.NEAREST)
        buff = BytesIO()
        new_img.save(buff, "GIF")
        canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
        canvas.configure(height=event.height, width=event.width)
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)

    # finally, bind that function so that it is called when the window is
    # resized.
    canvas.bind("<Configure>", on_resize)
    toplevel.bind(
        "<Configure>", lambda e: canvas.configure(height=e.height, width=e.width)
    )


COLORS = {
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "green": (0, 100, 0),
    "lime": (0, 255, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "yellow": (255, 230, 0),
    "purple": (179, 0, 199),
    "pink": (255, 0, 255),
    "orange": (255, 77, 0),
    "brown": (66, 52, 0),
    "grey": (152, 152, 152),
}


## SHAPES!


class Shape:
    # All subclasses MUST implement the following:
    #
    # __contains__(self, p) returns True if point p
    #   is inside the self shape
    #
    # center attribute or property for (x,y) center point
    #
    # draw method: draw the shape in a given color on a given image
    pass


class Circle(Shape):
    pass


class Rectangle(Shape):
    pass


if __name__ == "__main__":
    tk_root = tkinter.Tk()

    out_image = new_image(500, 500)

    shapes = []

    for (shape, color) in shapes:
        shape.draw(out_image, color)

    show_image(out_image, scale=1)

    tk_root.mainloop()