#!/usr/bin/env python
"""
Generic python script.
"""
from __future__ import print_function
import os
import importlib
import yaml

SKIP = [
    'bfg',
    'cfitsio',
    'ds9','pkgw-forge::ds9',
    'geos',
    'git',
    'iraf',
    'ipython',
    'kadrlica::oracle-instantclient',
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

COLORS = {
    'OK': '\033[92m',
    'WARN': '\033[93m',
    'FAIL': '\033[91m',
    'END': '\033[0m',
}

RETURN = {
    'ok': COLORS['OK']+"Success"+COLORS['END'],
    'fail': COLORS['FAIL']+"Failed"+COLORS['END'],
    'warn': COLORS['WARN']+"Warning"+COLORS['END'],
}

def test_modules(deps):
    print("Testing modules... ")
    for i,module in enumerate(deps):
        if isinstance(module,dict):
            for key,val in module.items():
                for mod in val:
                    test_import(mod)
        else:
            module = module.split('=')[0].strip()
            test_import(module)

        if module in list(TESTS.keys()): 
            print("  ", end="")
            TESTS[module]()

def test_import(module):
    module = module.split('=')[0]
    if module in SKIP: 
        return

    module = MAPPING.get(module,module)
    print("import %s... "%module, end="")
    try:
        importlib.import_module(module)
        print(RETURN['ok'])
    except ImportError as e:
        print(RETURN['fail'])
        print("  ImportError: %s"%e)

def test_matplotlib():
    print("Testing matplotlib figures... ",end="")
    import os
    import matplotlib
    import pylab as plt
    if os.getenv('DISPLAY') is None: 
        plt.switch_backend('Agg')
    #print("matplotlib backend: %s"%matplotlib.get_backend())
    plt.ion()
    plt.figure()
    plt.close('all')
    print(RETURN['ok'])

def test_esutil():
    print("Testing esutil... ",end="")
    import esutil
    try:
        esutil.test()
    except:
        print(RETURN['fail'])
    else:
        print(RETURN['ok'])

TESTS = {
    'matplotlib': test_matplotlib,
    'esutil': test_esutil,
}
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('env')
    args = parser.parse_args()
    
    env = yaml.safe_load(open(args.env))
    print("Testing: %s"%env['name'])
    deps = env['dependencies']
    
    # Test all the imports
    test_modules(deps)
