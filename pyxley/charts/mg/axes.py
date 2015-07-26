from .mg import OptionHelper

class Axes(OptionHelper):
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
        self.set_float("inflator", value)

    def set_xlim(self, xlim):
        if len(xlim) != 2:
            raise ValueError("xlim must contain two elements")

        if xlim[1] < xlim[0]:
            raise ValueError("Min must be less than Max")

        self.options["min_x"] = xlim[0]
        self.options["max_x"] = xlim[1]

    def set_ylim(self, ylim):
        if len(ylim) != 2:
            raise ValueError("ylim must contain two elements")

        if ylim[1] < ylim[0]:
            raise ValueError("Min must be less than Max")

        self.options["min_y"] = ylim[0]
        self.options["max_y"] = ylim[1]

    def set_min_y_from_data(self, value):
        self.set_boolean("min_y_from_data", value)

    def show_year_markers(self, value):
        self.set_boolean("show_year_markers", value)

    def show_secondary_x_label(self, value):
        self.set_boolean("show_secondary_x_label", value)

    def set_small_text(self, value):
        self.set_boolean("small_text", value)

    def show_x_extended_ticks(self, value):
        self.set_boolean("x_extended_ticks", value)

    def show_y_extended_ticks(self, value):
        self.set_boolean("y_extended_ticks", value)

    def show_xaxis(self, value):
        self.set_boolean("x_axis", value)

    def show_yaxis(self, value):
        self.set_boolean("y_axis", value)

    def set_xlabel(self, label):
        self.set_string("x_label", label)

    def set_ylabel(self, label):
        self.set_string("x_label", label)

    def set_xticks_count(self, value):
        self.options["xax_count"] = value

    def set_yticks_count(self, value):
        self.options["yax_count"] = value

    def xaxis_start_at_min(self, value):
        self.set_boolean("xax_start_at_min", value)

    def set_xticks_length(self, value):
        self.set_integer("xax_tick_length", value)

    def set_yticks_length(self, value):
        self.set_integer("yax_tick_length", value)

    def set_xunits(self, value):
        self.set_string("xax_units", value)

    def set_yunits(self, value):
        self.set_string("yax_units", value)

    def logscale(self):
        self.set_boolean("y_scale_type", True)

    def set_xformat(self, value):
        self.set_string("xax_format", value)

    def set_yformat(self, value):
        self.set_string("yax_format", value)

    def get(self):
        return {k:v for k,v in list(self.options.items()) if k in self._allowed_axes}

