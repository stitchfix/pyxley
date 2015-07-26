from ..ui import UIComponent

class Filter(UIComponent):
    name = "Filter"

class DownloadButton(Filter):
    """
    """
    def __init__(self, label, url, route_func):
        opts = {
            "url": url,
            "label": label
        }
        super(DownloadButton, self).__init__(
            "DownloadButton",
            opts,
            route_func)

class ConditionalButton(Filter):
    """
    """
    def __init__(self, labels, items, filter_ids, defaults,
                 filter_style="btn-group"):

        if (len(labels) != 2) or (len(defaults) != 2) or (len(filter_ids) != 2):
            raise Exception("The length of labels, defaults, or filter_ids must be 2")

        item_data = []
        for k, v in list(items.items()):
            item_data.append({"primary": k, "secondary": v})

        opts = {
            "labels": labels,
            "defaults": defaults,
            "aliases": filter_ids,
            "items": item_data,
            "filter_style": filter_style
        }
        super(ConditionalButton, self).__init__("ConditionalSelectButton", opts, None)

class SliderInput(Filter):
    """
    """
    def __init__(self, label, min_val, max_val, filter_id, default, step=1):
        opts = {
            "label": label,
            "min": min_val,
            "max": max_val,
            "step": step,
            "alias": filter_id,
            "default": default

        }
        super(SliderInput, self).__init__("SliderInput", opts, None)

class SelectButton(Filter):
    """
    """
    def __init__(self, label, items, filter_id, default):
        opts = {
            "label": label,
            "items": items,
            "alias": filter_id,
            "default": default
        }
        super(SelectButton, self).__init__("SelectButton", opts, None)

class ApiButton(Filter):
    """
    """
    def __init__(self, label, url, filter_id, default, route_func):
        opts = {
            "label": label,
            "url": url,
            "alias": filter_id,
            "default": default
        }
        super(ApiButton, self).__init__(
            "ApiButton",
            opts,
            route_func)

class DynamicTextInput(Filter) :
    """
    """
    def __init__(self, url, filter_id, default, route_func,
            placeholder="Enter text...", help=""):
        opts = {
            "url": url,
            "help": help,
            "alias": filter_id,
            "default": default,
            "placeholder": placeholder,
            "max": 20
        }
        super(DynamicTextInput, self).__init__(
            "DynamicSearch",
            opts,
            route_func)

