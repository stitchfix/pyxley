from .mg import OptionHelper

class Axes(OptionHelper):
    """Axes object for metricgraphics.

        This class is used to specify axes options for the metricsgraphics api.
        https://github.com/mozilla/metrics-graphics/wiki/Axes
    """
    _allowed_axes = [
        "inflator",
        "max_x", "max_y",
        "min_x", "min_y",
        "min_y_from_data",
        "missing_text",
        "show_missing_background",
        "show_year_markers",
        "show_secondary_x_label",
        "small_text",
        "xax_count",
        "xax_format",
        "x_axis",
        "x_extended_ticks",
        "x_label",
        "xax_start_at_min",
        "xax_units",
        "xax_tick_length",
        "y_axis",
        "y_extended_ticks",
        "y_label",
        "y_scale_type",
        "yax_count",
        "yax_format",
        "yax_tick_length",
        "yax_units"
        ]

    def set_inflator(self, value):
        """ Set inflator value.

            Args:
                value (float): inflator value.

        """
        self.set_float("inflator", value)

    def set_xlim(self, xlim):
        """ Set x-axis limits.

            Accepts a two-element list to set the x-axis limits.

            Args:
                xlim (list): lower and upper bounds

            Raises:
                ValueError: xlim must contain two elements
                ValueError: Min must be less than max
        """
        if len(xlim) != 2:
            raise ValueError("xlim must contain two elements")

        if xlim[1] < xlim[0]:
            raise ValueError("Min must be less than Max")

        self.options["min_x"] = xlim[0]
        self.options["max_x"] = xlim[1]

    def set_ylim(self, ylim):
        """ Set y-axis limits.

            Accepts a two-element list to set the y-axis limits.

            Args:
                ylim (list): lower and upper bounds

            Raises:
                ValueError: ylim must contain two elements
                ValueError: Min must be less than max
        """
        if len(ylim) != 2:
            raise ValueError("ylim must contain two elements")

        if ylim[1] < ylim[0]:
            raise ValueError("Min must be less than Max")

        self.options["min_y"] = ylim[0]
        self.options["max_y"] = ylim[1]

    def set_min_y_from_data(self, value):
        """ Set flag to find the minimum y-value from the data."""
        self.set_boolean("min_y_from_data", value)

    def show_year_markers(self, value):
        """ Set flag to show year markers."""
        self.set_boolean("show_year_markers", value)

    def show_secondary_x_label(self, value):
        """ Set flag to show secondary x label."""
        self.set_boolean("show_secondary_x_label", value)

    def set_small_text(self, value):
        """ Set flag to show small text."""
        self.set_boolean("small_text", value)

    def show_x_extended_ticks(self, value):
        """ Set flag to show extended x-axis tick marks."""
        self.set_boolean("x_extended_ticks", value)

    def show_y_extended_ticks(self, value):
        """ Set flag to show extended y-axis tick marks."""
        self.set_boolean("y_extended_ticks", value)

    def show_xaxis(self, value):
        """ Set flag to show x-axis."""
        self.set_boolean("x_axis", value)

    def show_yaxis(self, value):
        """ Set flag to show y-axis."""
        self.set_boolean("y_axis", value)

    def set_xlabel(self, label):
        """ Set x-axis label."""
        self.set_string("x_label", label)

    def set_ylabel(self, label):
        """ Set y-axis label."""
        self.set_string("x_label", label)

    def set_xticks_count(self, value):
        """ Set xticks counts."""
        self.options["xax_count"] = value

    def set_yticks_count(self, value):
        """ Set yticks counts."""
        self.options["yax_count"] = value

    def xaxis_start_at_min(self, value):
        """ Set flag to start x-axis at the min value."""
        self.set_boolean("xax_start_at_min", value)

    def set_xticks_length(self, value):
        """ Set the length of the x-axis ticks."""
        self.set_integer("xax_tick_length", value)

    def set_yticks_length(self, value):
        """ Set the length of the y-axis ticks."""
        self.set_integer("yax_tick_length", value)

    def set_xunits(self, value):
        """ Set the units on the x-axis."""
        self.set_string("xax_units", value)

    def set_yunits(self, value):
        """ Set the units on the y-axis."""
        self.set_string("yax_units", value)

    def logscale(self):
        """ Set flag to log scale the y-axis."""
        self.set_boolean("y_scale_type", True)

    def set_xformat(self, value):
        """ Set the x-axis format."""
        self.set_string("xax_format", value)

    def set_yformat(self, value):
        """ Set the y-axis format."""
        self.set_string("yax_format", value)

    def get(self):
        """ Retrieve options set by user."""
        return {k:v for k,v in list(self.options.items()) if k in self._allowed_axes}

