from .mg import OptionHelper

class Layout(OptionHelper):
    _allowed_layout = [
        "buffer",
        "bottom",
        "height",
        "left",
        "right",
        "small_height_threshold",
        "small_width_threshold",
        "top",
        "width"
    ]

    def set_margin(self, top=40, bottom=30, left=50, right=10, buffer_size=8):
        self.set_integer("top", top)
        self.set_integer("bottom", bottom)
        self.set_integer("left", left)
        self.set_integer("right", right)
        self.set_integer("buffer", buffer_size)

    def set_size(self, height=220, width=350,
                 height_threshold=120,
                 width_threshold=160):
        self.set_integer("height", height)
        self.set_integer("width", width)
        self.set_integer("small_height_threshold", height_threshold)
        self.set_integer("small_width_threshold", width_threshold)

    def get(self):
        return {k:v for k,v in list(self.options.items()) if k in self._allowed_layout}