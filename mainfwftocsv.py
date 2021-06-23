from string import capwords
from filespecclass import *
from makefwf import *
import sys
import re
from functools import partial
import os


SPEC_FILENAME = 'spec.json'
FIX_FILENAME = "newfile.txt"
N_RECORDS = 10000
CHUNK = 1000


def write_header(infile, outfile, spec1:spec_class):    
    # This function writes header line to csv  file
    infile.readline()
    header =bytearray()
    index = 0
    for column, _ in spec1.columns:
        header += column.encode(spec1.delimited_encoding)
        index += 1
        if index < len(spec1.columns):
            header += b','
    header += b'\n'    
    outfile.write(header.decode(spec1.delimited_encoding))


def make_pattern(columns):
    #Create pattern to read fwf file by regex
    pattern=''
    for _, offset in columns:
        pattern +='(.{' + str(offset) + '})'
    return pattern

def create_delimited_file(fixfilename: str, csvfilename: str, spec: spec_class, pattern: str, chunk: int):
    #Read fwf file and writes to csv file
    csv_encoding = spec.delimited_encoding
    fix_encoding = spec.fixedwidth_encoding
    # open two files to read and write
    with open(fixfilename,'r', encoding=fix_encoding) as fixfile:
        print("Reading fwf file ..... ")
        print("Writing csv file ..... ")
        with open(csvfilename,'w',encoding=csv_encoding) as csvfile:
            #make header line of csv file
            if spec.include_header:
                write_header(fixfile,csvfile, spec)
            #read each line and add to bytearray
            line_counter = 0
            sum_lines = bytearray()
            #read line by line, extract records and write to csv file
            for line in fixfile:
                rec = re.findall(pattern , line)[0]
                fields = [*map(partial(str.encode, encoding=csv_encoding) , rec)]
                sum_lines += b','.join(fields)
                sum_lines += b'\n'
                line_counter +=1
                if line_counter == chunk:
                    csvfile.write(sum_lines.decode(csv_encoding))
                    print(f"writing {line_counter} lines to csv file.")
                    line_counter = 0
                    sum_lines = bytearray()
            if line_counter != 0:
                csvfile.write(sum_lines.decode(csv_encoding))
                print(f"writing {line_counter} lines to csv file.")
    print(f'Fixed width file converted to {csvfilename} with {N_RECORDS} rows in the output directory.')


if __name__ == '__main__':
    #reading command line arguments
    nargs = len(sys.argv)
    if nargs <4 :
        print("Format  : python mainfwftocsv.py numberofrecords newfilename specfile")
        print("Default : python mainfwftocsv.py 5000 newfile spec.json")
    message = "bad argument"
    try:
        if nargs >=2 :
            message = "bad argument1"
            N_RECORDS = int(sys.argv[1])
        if nargs >=3 :
            message = "bad argument2"
            FIX_FILENAME = sys.argv[2]
        if nargs >=4 :
            message = "bad argument3"
            SPEC_FILENAME = sys.argv[3]        
    except:
        print(message)
        sys.exit()

    #Make output folder
    if not os.path.isdir('./output'):
        os.mkdir('output')
    # make output csv filename
    csv_filename=FIX_FILENAME.split('.')[0]+'.csv'
    FIX_FILENAME='./output/' + FIX_FILENAME
    csv_filename = './output/' + csv_filename

    #read spec file
    filespec = spec_class('./input/'+SPEC_FILENAME)
    if filespec == None :
        sys.exit()
    
    #make record pattern
    pattern = make_pattern(filespec.columns)
    #create fixed width file
    create_fixedwidthfile(FIX_FILENAME, filespec, N_RECORDS, CHUNK)   
    #read fix width file and write deleimited csv file
    create_delimited_file(FIX_FILENAME, csv_filename, filespec, pattern, CHUNK)