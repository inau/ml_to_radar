The data in this directory is a subset.
It is nowhere as extensive as the data used in the real investigation.
However one can run the different python scripts on the data to test them.

Examples:
##	Extracting samples from raw data:
	Cmd:	python permute.py target_directory source_directory
	Out:	Will produce the target_directory with samples.
		
##	Testing the networks:
	Cmd:	python ml.py training_dir test_dir
	Out:	mlstats/ directory with csv data
	
##	Running max_predict
	Do note: 	this is written as a module and is used differently
				If one does not want to change the path it is possible to use relative paths.
				
				Data has 2 second scan time and the stat script is using this setting(hardcoded).
				
	Cmds: 	python
			import max_predict as mp
			
	statistics:
			mp.predict_stats('filepath', 'out_file_name')
	or single file:	
			mp.predict('csv_filename', scan_time)