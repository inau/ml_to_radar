#!/bin/bash

# Get the basename of xml file, omit extension
base=`basename $1 .fersxml`
mkdir -p $base
# Get parent directory name
par=${PWD##*/}
cd $base
# Execute sim, redirect stdout and stderr to logfile
../../../../bin/fers ../$base.fersxml > $base.log 2>&1
echo 'Simulation performed '$base' in '$par
