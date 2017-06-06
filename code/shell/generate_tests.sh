#!/bin/bash
if test -e "test.meta";
then
	# Extract variation params (# of tests, delta x, delta y)
	in=$(head -1 test.meta)	
	in1=$(head -2 test.meta)	
	in2=$(head -3 test.meta)	
	tests=${in##*=}
	dx=${in1##*=}
	dy=${in2##*=}

	# Loop number of tests
	for n in $(seq $tests)
	do
		# Get X and Y for this test
		nx=$((dx*n))
		ny=$((dy*n))
		# Replace target tags with targets.xml if present and generate intermediary
		if test -e "targets.xml";
			then
				val=`cat targets.xml`
				sed  '/<TARGETS>/ {r targets.xml
				d} ' test.meta > test.intermediary
			else
				cat test.meta > test.intermediary
		fi
		# Ommit the first 3 lines of the intermediary and validate fersxml
		# do sed replacement on dynamic targets
		tail -n +4 test.intermediary | xmllint --xinclude --output test${n}.fersxml --noent -
		sed -i 's/<dxp>0.0<\/dxp>/<x>'"$nx"'<\/x>/' test${n}.fersxml
		sed -i 's/<dxn>0.0<\/dxn>/<x>'"-$nx"'<\/x>/' test${n}.fersxml
		sed -i 's/<dyp>0.0<\/dyp>/<y>'"$ny"'<\/y>/' test${n}.fersxml
		sed -i 's/<dyn>0.0<\/dyn>/<y>'"-$ny"'<\/y>/' test${n}.fersxml

	done
	echo 'FERSXML files generated, running tests'
fi