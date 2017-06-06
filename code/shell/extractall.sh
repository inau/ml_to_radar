#!/bin/bash

# Targetfolder - create log file aswell
base='sampledata' 
mkdir -p $base
touch $base/test.txt
for dir in `find . -maxdepth 1 -mindepth 1 -type d`; do
  # Ignore the new directory and the general settings
  if [ "$dir" != "./_general" ] && [ "$dir" != "./$base" ]
  then
	# Treat every testcategory as a label
	label=`basename $dir`
	echo $label
	# Prepare target folder
	mkdir -p $base/$label
	cd $dir
	# Lookup and logging
	data=`ls */*mono1.csv`
	echo $dir' \n\n' >> ../$base/test.txt
	echo $data >> ../$base/test.txt
	c=1
	# Copy all data files and rename them
	for d in $data; do
		cp -- "$d" ../$base/$label/$c.csv 
		c=$((c+1))
	done
	cd ..
  fi
done
