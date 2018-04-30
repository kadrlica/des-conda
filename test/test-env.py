#!/usr/bin/env python
"""
Generic python script.
"""
__author__ = "Alex Drlica-Wagner"
import os
import importlib
import yaml

SKIP = [
    'ds9',
    'geos',
    'git',
    'iraf',
    'ipython',
    'proj4',
    'python',
    'r',
    'r-essentials',
    'r-ggplot2',
    'r-irkernel',
    'r-mapproj',
    'r-rpostgresql',
    'sqlite',
    'svn',
    ]
    
MAPPING = {
    'basemap':'mpl_toolkits.basemap',
    'beautifulsoup4':'bs4',
    'cx_oracle':'cx_Oracle',
    'netcdf4':'netCDF4',
    'python-redmine':'redminelib',
    'pyyaml':'yaml',
    'scikit-image':'skimage',
    'scikit-learn':'sklearn',
    'spherical-geometry':'spherical_geometry',
    }

def test_import(module):
    module = module.split('=')[0]
    if module in SKIP: 
        return

    module = MAPPING.get(module,module)
    try:
        importlib.import_module(module)
        print("Success: import %s"%module)
    except ImportError as e:
        print("Failure: import %s"%module)
        print("  ImportError: %s"%e)

def test_matplotlib():
    import os
    import matplotlib
    if not os.getenv('DISPLAY'): matplotlib.use('Agg')
    import pylab as plt
    plt.ion()
    plt.figure()
    plt.close('all')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('env')
    args = parser.parse_args()
    
    env = yaml.load(open(args.env))
    print("Testing: %s"%env['name'])
    deps = env['dependencies']

    for i,module in enumerate(deps):
        if isinstance(module,dict):
            for key,val in module.items():
                for mod in val:
                    test_import(mod)
        else:
            test_import(module)

    # Other specific tests
    test_matplotlib()
