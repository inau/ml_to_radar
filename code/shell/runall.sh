#!/bin/bash

for dir in `find . -maxdepth 1 -mindepth 1 -type d`; do
  if [ "$dir" != "./_general" ]
  then
	cd $dir
	sh ../../../util/generate_tests.sh
	find -name "test*.fersxml" -exec ../../../util/runtest.sh '{}' \;
	cd ..
  fi
done