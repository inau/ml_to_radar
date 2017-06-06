#!/bin/bash

for dir in `find . -maxdepth 1 -mindepth 1 -type d`; do
  if [ "$dir" != "./_general" ]
  then
	par=${PWD##*/}
	cd $dir && gnuplot -e "tt='$par'" ../../../util/plotCSV_mul.plt
	tts =
	for subdir in `find -name "test*.fersxml"`; do
		base=`basename $subdir .fersxml`
		cd $base
		gnuplot -e "filename='mono1_results_mono1.csv';cfar='$cfar'; tt='$par'; tn='$base'" ../../../../util/plotCSV.plt
		cd ..
	done
	cd ..
  fi
done

#find -name "test*.fersxml" -exec ./runtest.sh '{}' \;
#Generate combined graphs for all tests
#gnuplot ../../util/plotCSV_mul_meta.plt
