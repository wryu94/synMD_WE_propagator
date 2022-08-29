#!/bin/bash

source env.sh

rm -f west.h5
BSTATES="--bstate initial,1"
TSTATES="--tstate final,2019.0"
$WEST_ROOT/bin/w_init $BSTATES $TSTATES "$@"
