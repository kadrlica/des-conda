#!/bin/bash

[ -z $XDG_RUNTIME_DIR ] && {
    export XDG_RUNTIME_DIR=$TMPDIR/runtime-$USER
}
