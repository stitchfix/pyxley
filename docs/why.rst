Why Pyxley?
===========

Pyxley was born out of the desire to combine the ease of data manipulation in pandas
with the beautiful visualizations available in JavaScript. It was largely inspired by
`Real Python <https://realpython.com/blog/python/the-ultimate-flask-front-end/>`_. The goal was to create a library of reusable visualization components
that allow the quick development of web-based data products. For data scientists with limited
JavaScript exposure, this package is meant to provide generic visualizations along with the
ability to customize as needed.

React
-----

Pyxley utilizes Facebook's `React <http://facebook.github.io/react/index.html>`_. React
is only concerned with the UI, so we can use it for only the front-end portion of our
web-applications.

Flask
-----
`Flask <https://readthedocs.org/projects/flask/>`_ is a great micro web-framework. It
allows us to very easily stand up web applications and services.

PyxleyJS
--------

Pyxley relies on a JavaScript library that heavily leverages React and existing
visualization libraries. Wrappers for common libraries have been created so that
the user only needs to specify the type of chart they want, the filters they wish
to include, and the parameters specific to that visualization.

To download or contribute, visit `PyxleyJS <http://www.github.com/stitchfix/pyxleyJS>`_.


Insane Templates
----------------

A lot of other projects rely on a set of complicated templates that attempt to cover
as many use cases as possible. The wonderful thing about React is the ability to create
compositions of components. This means that we only need a single template: a parent component that manages all of the child components. With this layout, we can use factories within JavaScript
to create the components using the supplied parameters. Organizing the code in this way
allows us to create a common framework through which we can create a variety of different
components.

For example, the underlying interface for a Dropdown Button and a Line Chart are
the same. The only difference is the options supplied by the user. This provides a really
easy way to integrate with Python. We can use Python for organizing the types and options.
PyReact can then be used to transform to JavaScript.


