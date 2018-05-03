1. dbus was not installing correctly in des17a. Needed to manually run post-link script:
$CONDA_PREFIX/bin/.dbus-post-link.sh
to add:
$CONDA_PREFIX/var/lib/dbus/machine_id