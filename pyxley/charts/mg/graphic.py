from .mg import OptionHelper

class Graphic(OptionHelper):
    """ Graphic options for the metricsgraphics api.

        This class contains all graphics options for the metricsgraphics api.
        https://github.com/mozilla/metrics-graphics/wiki/Graphic

    """
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

    _allowed_charts = ["line", "histogram", "point", "bar", "missing-data"]

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
        """Set the MetricsGraphics chart type.
            Allowed charts are: line, histogram, point, and bar

            Args:
                value (str): chart type.

            Raises:
                ValueError: Not a valid chart type.
        """
        if value not in self._allowed_charts:
            raise ValueError("Not a valid chart type")

        self.options["chart_type"] = value

    def custom_line_color_map(self, values):
        """Set the custom line color map.

            Args:
                values (list): list of colors.

            Raises:
                TypeError: Custom line color map must be a list.
        """
        if not isinstance(values, list):
            raise TypeError("custom_line_color_map must be a list")

        self.options["custom_line_color_map"] = values

    def decimals(self, value):
        """Set the number of decimals to display."""
        self.set_integer("decimals", value)

    def error(self, value):
        """Set the error message."""
        self.set_string("error", value)

    def format(self, value):
        """Set the format type.
            Allowed charts are: count or percentage

            Args:
                value (str): format type.

            Raises:
                ValueError: Not a valid format. Must be count or percentage.
        """
        if value not in ["count", "percentage"]:
            raise ValueError("Not a valid format. Must be count or percentage")

        self.options["format"] = value

    def full_height(self):
        """Use full height?"""
        self.set_boolean("full_height", True)

    def full_width(self):
        """Use full width?"""
        self.set_boolean("full_width", True)

    def interpolate(self, value):
        """Set the interpolate type.
            See metricsgraphics documentation for interpolate types
            https://github.com/mozilla/metrics-graphics/wiki/List-of-Options

            Args:
                value (str): interpolate type.

            Raises:
                ValueError: Not a valid interpolation method.
        """
        if value not in _allowed_interpolates:
            raise ValueError("Not a valid interpolation method")

        self.options["interpolate"] = value

    def interpolate_tension(self, value):
        """Set the interpolate tension.

            Args:
                value (str): interpolate type.

            Raises:
                ValueError: Tension must in [0, 1].
        """
        if (value < 0) or (value > 1):
            raise ValueError("Tension must in [0, 1]")

        self.options["interpolate_tension"] = value

    def legend(self, values):
        """Set the legend labels.

            Args:
                values (list): list of labels.

            Raises:
                ValueError: legend must be a list of labels.
        """
        if not isinstance(values, list):
            raise TypeError("legend must be a list of labels")

        self.options["legend"] = values

    def legend_target(self, value):
        """Set the legend target."""
        self.set_string("legend_target", value)

    def linked(self):
        """Link the charts?"""
        self.set_boolean("linked", True)

    def linked_format(self, value):
        """Set the link format."""
        self.set_string("linked_format", value)

    def as_list(self):
        """Set flag to automatically map the data to x and y accessors."""
        self.set_boolean("list", True)

    def markers(self, values):
        """Set the markers.

            Args:
                values (list): list of marker objects.

            Raises:
                ValueError: Markers must be a list of objects.
        """
        if not isinstance(values, list):
            raise TypeError("Markers must be a list of objects")

        self.options["markers"] = values

    def max_data_size(self, value):
        """Set the max data size."""
        self.set_integer("max_data_size", value)

    def missing_text(self, value):
        """Set the text for missing graphics."""
        self.set_string("missing_text", value)

    def show_missing_background(self, value=True):
        """Display a background for missing graphics?"""
        self.set_boolean("show_missing_background", value)

    def point_size(self, value):
        """Set the point size."""
        self.set_float("point_size", value)

    def show_confidence_band(self, value):
        """Show confidence band?
            See metricsgraphics documentation
            Args:
                value (list): strings

            Raises:
                TypeError: show_confidence_band must be a list of strings.
        """
        if not isinstance(values, list):
            raise TypeError("show_confidence_band must be a list of strings")

        self.options["show_confidence_band"] = values

    def show_rollover_text(self, value=True):
        """Show rollover text?"""
        self.set_boolean("show_rollover_text", value)

    def show_tooltips(self, value=True):
        """Show tooltips?"""
        self.set_boolean("show_tooltips", value)

    def target(self, value):
        """Set target."""
        self.set_string("target", value)

    def transition_on_update(self, value=True):
        """Transition on update?"""
        self.set_boolean("transition_on_update", value)

    def x_rug(self):
        self.set_boolean("x_rug", True)

    def y_rug(self):
        self.set_boolean("y_rug", True)

    def get(self):
        """Get graphics options."""
        return {k:v for k,v in list(self.options.items()) if k in self._allowed_graphics}
