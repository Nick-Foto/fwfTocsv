filespecclass.py
	Define a class for reading spec file and extracting column headers and field lenghts

makefwf.py
	create fix width file using spec file pattern and number of records defined by user

mainfwftocsv.py
	main program including:
		1 - read spec file and extracting pattern and fields
		2 - make pattern of records (lines)
		3 - create a fixed width file with random data using the provided spec
		4 - read the fixedwidthfile and convert it to a csv file

input :
	These programs read specfile as input file from "input" folder.
output : 
	These programs write output files to a foler named "output".


To run program by default arguments :  python mainfwftocsv.py

To run program by arguments :  python3 mainfwftocsv.py  numberofrecords newfilename  specfilename

dDefault arguments are :
	numberofrecords : 10000
	newfilename     : newfile
	specfilename    : spec.json