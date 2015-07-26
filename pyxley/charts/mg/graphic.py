from .mg import OptionHelper

class Graphic(OptionHelper):
    _allowed_graphics = [
        "aggregate_rollover",
        "animate_on_load",
        "area",
        "baselines",
        "chart_type",
        "custom_line_color_map",
        "decimals",
        "error",
        "format",
        "full_height",
        "full_width",
        "interpolate",
        "interpolate_tension",
        "legend",
        "legend_target",
        "linked",
        "lined_format",
        "list",
        "markers",
        "max_data_size",
        "mouseover",
        "mousemove",
        "mouseout",
        "point_size",
        "show_confidence_band",
        "show_rollover_text",
        "show_tooltips",
        "target",
        "transition_on_update",
        "x_rug",
        "y_rug"
    ]

    _allowed_charts = ["line", "histogram", "point", "missing-data"]

    _allowed_interpolates = [
        "cardinal",
        "linear",
        "linear-closed",
        "step",
        "step-before",
        "step-after",
        "basis",
        "basis-open",
        "basis-closed",
        "bundle",
        "cardinal-open",
        "cardinal-closed",
        "monotone"
    ]

    def aggregate_rollover(self):
        self.set_boolean("aggregate_rollover", True)

    def animate_on_load(self):
        self.set_boolean("animate_on_load", True)

    def area(self, value=True):
        self.set_boolean("area", value)

    def add_baseline(self, value, label="baseline"):
        self.options["baselines"] = [{"value": value, "label": label}]

    def chart_type(self, value):
        if value not in self._allowed_charts:
            raise ValueError("Not a valid chart type")

        self.options["chart_type"] = value

    def custom_line_color_map(self, values):
        if not isinstance(values, list):
            raise TypeError("custom_line_color_map must be a list")

        self.options["custom_line_color_map"] = values

    def decimals(self, value):
        self.set_integer("decimals", value)

    def error(self, value):
        self.set_string("error", value)

    def format(self, value):
        if value not in ["count", "percentage"]:
            raise ValueError("Not a valid format. Must be count or percentage")

        self.options["format"] = value

    def full_height(self):
        self.set_boolean("full_height", True)

    def full_width(self):
        self.set_boolean("full_width", True)

    def interpolate(self, value):
        if value not in _allowed_interpolates:
            raise ValueError("Not a valid interpolation method")

        self.options["interpolate"] = value

    def interpolate_tension(self, value):
        if (value < 0) or (value > 1):
            raise ValueError("Tension must in [0, 1]")

        self.options["interpolate_tension"] = value

    def legend(self, values):
        if not isinstance(values, list):
            raise TypeError("legend must be a list of labels")

        self.options["legend"] = values

    def legend_target(self, value):
        self.set_string("legend_target", value)

    def linked(self):
        self.set_boolean("linked", True)

    def linked_format(self, value):
        self.set_string("linked_format", value)

    def as_list(self):
        self.set_boolean("list", True)

    def markers(self, values):
        if not isinstance(values, list):
            raise TypeError("Markers must be a list of objects")

        self.options["markers"] = values

    def max_data_size(self, value):
        self.set_integer("max_data_size", value)

    def missing_text(self, value):
        self.set_string("missing_text", value)

    def show_missing_background(self, value=True):
        self.set_boolean("show_missing_background", value)

    def point_size(self, value):
        self.set_float("point_size", value)

    def show_confidence_band(self, value):
        if not isinstance(values, list):
            raise TypeError("show_confidence_band must be a list of strings")

        self.options["show_confidence_band"] = values

    def show_rollover_text(self, value=True):
        self.set_boolean("show_rollover_text", value)

    def show_tooltips(self, value=True):
        self.set_boolean("show_tooltips", value)

    def target(self, value):
        self.set_string("target", value)

    def transition_on_update(self, value=True):
        self.set_boolean("transition_on_update", value)

    def x_rug(self):
        self.set_boolean("x_rug", True)

    def y_rug(self):
        self.set_boolean("y_rug", True)

    def get(self):
        return {k:v for k,v in list(self.options.items()) if k in self._allowed_graphics}
