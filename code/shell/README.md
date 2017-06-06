*******************************************************************************************
[**[** the script structure is not 1:1 so wont work until the relative path is fixed **]**]
*******************************************************************************************

	extractall.sh:
		extract all csv files from a directory and its subdirectory into a folder
		
	runtest.sh:
		create a folder with the basename of the fersxml file
		cd into it, and execute the fers binary
		
	runall.sh:
		example of shellscript that traverses a fers meta dir.
		ignores the _general folder as this by convention has no .meta files
		traverse all others dirs
			use 'generate_tests.sh' on .meta 
		once done find all fers.xml and run 'runtest.sh'
		
	generate_tests.sh:
		looks for a valid meta file in the directory
		does different bash replacements and validations.
		
	graphall.sh:
		A script that traverses a fers meta dir and runs different gnuplot scripts on it.
		