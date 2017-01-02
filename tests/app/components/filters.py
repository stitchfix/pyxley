
from pyxley.filters import *

def get_api_button():
    """ basic api button

        get a dropdown populated by an api

        Args:
            url (str): endpoint to call upon click.
    """
    return ApiButton(
        "Api Button",
        "/api/api_button/",
        "api_button",
        "selection",
        None
    )

def get_select_button():
    """ select button

        get a dropdown populated by a list
    """
    return SelectButton(
        "Select Button",
        ["Selection {}".format(i) for i in range(1,6)],
        "select_button",
        "Selection 1"
    )

def get_download_button():
    """ download button

        get a download button

        Args:
            url (str): endpoint to call upon click.
            endpoint_func (function): function to call upon click.
    """
    return DownloadButton(
        "Download",
        "/api/download/",
        None
    )

def get_slider_input():
    """ slider input

        get a slider.
    """
    return SliderInput(
        "Slider Input", 1, 10, "slider_input", "1"
    )
