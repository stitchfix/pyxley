from ..ui import UIComponent

class Filter(UIComponent):
    """Base class for Filter UIComponent"""
    name = "Filter"

class DownloadButton(Filter):
    """Download Button.

        A simple download button.

        Args:
            label (str): label of the button.
            url (str): endpoint to call upon click.
            route_func (function): endpoint function.

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
    """Conditional Button Group.

        A group of two buttons where the parent choice affects
        the child choice.

        Args:
            labels (list): labels of the button.
            items (dict): choices, children are nested.
            filter_ids (list): list of aliases for the filter.
            defaults (list): default selections.
            filter_style: css for the buttons.

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
    """Simple Slider input.

        A slider bar.

        Args:
            label (str): label of the slider.
            min_val (int): minimum value.
            max_val (int): maximum value.
            filter_id (str): list of aliases for the filter.
            default (int): default selection.
            step (int): size of the step associated with the slider.

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
    """Dropdown Button.

        A dropdown selection button based on the React-Bootstrap Dropdown.
        http://react-bootstrap.github.io/components.html#buttons

        Args:
            label (str): label of the button.
            items (dict): choices, children are nested.
            filter_id (str): alias of the filter.
            default (str): default selection.

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
    """Selections populated by API.

        A dropdown selection button based on the React-Bootstrap Dropdown.
        http://react-bootstrap.github.io/components.html#buttons

        The selections are created by calling an endpoint.

        Args:
            label (str): label of the button.
            url (str): name of endpoint to create.
            filter_id (str): alias of the filter.
            default (str): default selection.
            route_func (function): endpoint function to serve the options.

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
    """Dynamic Text Selection.

        A combination search bar plus drop down inspired by:
        https://realpython.com/blog/python/the-ultimate-flask-front-end-part-2/

        The selections are created by calling an endpoint.

        Args:
            url (str): name of endpoint to create.
            filter_id (str): alias of the filter.
            default (str): default selection.
            route_func (function): endpoint function to serve the options.
            placeholder (str): default text.
            help (str): help text.

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

class ReactSelect(Filter):
    """ react-select wrapper

        This is a wrapper for the react-select library
        http://jedwatson.github.io/react-select/

        Args:
            url (str): name of endpoint to create.
            filter_id (str): alias of the filter.
            default (str): default selection.
            route_func (function): endpoint function to serve the options.
            placeholder (str): default text.
            extra_args (dict): extra props.
    """
    def __init__(self, url, filter_id, default, route_func,
            placeholder="Enter text...", extra_args={}):
        opts = {
            "url": url,
            "alias": filter_id,
            "default": default,
            "options": {
                "placeholder": placeholder
            }
        }
        for arg in extra_args:
            opts["options"][arg] = extra_args[arg]

        super(ReactSelect, self).__init__("ReactSelect", opts, route_func)

    @staticmethod
    def format_options(opts):
        return {
            "data": [{"label": k, "value": k} for k in opts]
        }
