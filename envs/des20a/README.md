Some notes:

1. qt5agg was not working due to opengl configuration issues:
https://github.com/ContinuumIO/anaconda-issues/issues/9229
Workaround is to change default backend to 'tkagg' in:
$CONDA_PREFIX/lib/python2.7/site-packages/matplotlib/mpl-data/matplotlibrc
Users should be aware of this change.

2. There was a warning about XDG_RUNTIME_DIR not being set. Fixed with:
$CONDA_PREFIX/etc/conda/activate.d/xdg.sh

3. CVMFS hates hardlinks. Specify that softlinks should always be used in ~/.condarc
always_softlink: True