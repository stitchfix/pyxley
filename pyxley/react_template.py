from react import jsx
from jinja2 import Template
import json

class ReactTemplate(object):
    """Base React class.

        This class handles the basic transformation of the React jsx code.
        It takes a dictionary of options, renders the template, and
        writes the transformed javascript file.

        Args:
            template (str): jinja2 template for the react jsx code.
            template_args (dict): options to be populated in the template.
            path (str): path of the file to create.
    """
    def __init__(self, template, template_args, path):
        self.transformer = jsx.JSXTransformer()
        self.template = template
        self.args = template_args
        self.path = path

    def write_to_file(self, s):
        """
        """
        f = open(self.path, 'w')
        f.write(s)
        f.close()

    def to_js(self):
        """
        """
        t = Template(self.template)
        js = self.transformer.transform_string(t.render(**self.args))
        self.write_to_file(js)

def format_props(props):
    """ Formats props for the React template.

        Args:
            props (dict): properties to be written to the template.

        Returns:
            Two lists, one containing variable names and the other
            containing a list of props to be fed to the React template.

    """
    vars_ = []
    props_ = []
    for k, v in list(props.items()):
        vars_.append(Template("var {{k}} = {{v}};").render(k=k,v=json.dumps(v)))
        props_.append(Template("{{k}} = {{v}}").render(k=k, v="{"+k+"}"))
    return "\n".join(vars_), "\n".join(props_)


class ReactComponent(ReactTemplate):
    """Class to generate javascript from parameters.

        This class create a javascript file by compiling a JSX string containing
        React components. A single parent component is rendered and sub-components
        are passed into the component as props.

        Args:
            name (str): name of the ReactComponent to create.
            path (str): location of the javascript file containing the component.
            element_id (str): html element id.
            props (dict): properties of the react component to render.
            static_path (str): output file destination.
    """
    _react = (
    """
    var Component = require("{{path}}").{{name}};
    {{vars}}
    React.render(
        <Component
        {{props}} />,
        document.getElementById("{{id}}")
    );
    """)
    def __init__(self, name, path, element_id, props={}, static_path=""):
        vars_, props_ = format_props(props)

        params = {
            "name": name,
            "path": path,
            "vars": vars_,
            "props": props_,
            "id": element_id
        }
        for k, v in list(props.items()):
            params[k] = v

        super(ReactComponent, self).__init__(
            self._react, params, static_path)
        self.to_js()


