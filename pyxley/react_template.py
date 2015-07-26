from react import jsx
from jinja2 import Template
import json

class ReactTemplate(object):
    """
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
    """
    """
    vars_ = []
    props_ = []
    for k, v in list(props.items()):
        if isinstance(v, bool):
            vars_.append(Template("var {{k}} = {{v|lower}};").render(k=k,v=v))
        elif isinstance(v, list) or isinstance(v, dict):
            vars_.append(Template("var {{k}} = {{v}};").render(k=k,v=json.dumps(v)))
        else:
            vars_.append(Template("var {{k}} = {{v}};").render(k=k,v=v))
        props_.append(Template("{{k}} = {{v}}").render(k=k, v="{"+k+"}"))
    return "\n".join(vars_), "\n".join(props_)


class ReactComponent(ReactTemplate):
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


