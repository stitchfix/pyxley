from setuptools import setup

setup(
    name='pyxley',
    version='0.0.8',
    author='Nicholas Kridler',
    author_email='nmkridler@gmail.com',
    license='MIT',
    description='Python tools for building Flask-based web applications',
    packages = ['pyxley', 'pyxley.filters', 'pyxley.charts', 'pyxley.charts.mg',
        'pyxley.charts.datatables', 'pyxley.charts.datamaps',
        'pyxley.charts.nvd3', 'pyxley.utils'],
    long_description='Python tools for building Flask-based web applications using React.js',
    url='https://github.com/stitchfix/pyxley',
    keywords=['pyreact', 'flask'],
    classifiers=[
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'flask',
        'pandas'
    ],
    scripts = [
        "bin/pyxapp"
    ]
)
