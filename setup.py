from setuptools import setup

setup(
    name='pyxley',
    version='0.1.0',
    author='Nicholas Kridler',
    author_email='nmkridler@gmail.com',
    license='MIT',
    description='Python tools for building Flask-based web applications',
    packages = ['pyxley', 'pyxley.filters', 'pyxley.charts', 'pyxley.charts.mg',
        'pyxley.charts.datatables', 'pyxley.charts.datamaps',
        'pyxley.charts.nvd3', 'pyxley.utils', 'pyxley.charts.plotly'],
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
    ],
    package_data = {
        'pyxley': ['LICENSE.txt', 'assets/bundle.js', 'assets/templates/index.html']
    },
    data_files=[
        ('assets', [
            'assets/bundle.js',
            'assets/templates/index.html',
            'assets/css/main.css'
        ])
    ],
    include_package_data=True
)
