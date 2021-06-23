from typing import ByteString
from filespecclass import *
import random
import string


def write_header(outfile, spec1:spec_class):    
    header = bytearray()
    for column, offset in spec1.columns:
        header += column.ljust(offset,' ').encode(spec1.fixedwidth_encoding)
    header += b'\n'
    outfile.write(header.decode(encoding=spec1.fixedwidth_encoding))


def create_fixedwidthfile(filename: string, file_spec: spec_class, n_records: int, chunk: int):
    fix_encoding = file_spec.fixedwidth_encoding
    print("Creating fwf file ..... ")
    with open(filename,'w', encoding=fix_encoding) as file:
        if file_spec.include_header:
            write_header(file, file_spec)
        sum_lines = bytearray()
        line_counter = 0
        for _ in range(n_records):
            for _, offset in file_spec.columns:
                str1=''.join(random.choices(string.ascii_letters+string.digits, k= offset))
                #str1="{0:<{length}}".format(str1,length=offset)
                str1=f"{str1:<{offset}}"
                sum_lines += str1.encode(encoding=fix_encoding)
            sum_lines += b'\n'
            line_counter += 1
            if line_counter == chunk:
                file.write(sum_lines.decode(fix_encoding))
                print(f"writing {line_counter} lines to fixed width file.")
                line_counter = 0
                sum_lines = bytearray()
        if line_counter != 0 :
            file.write(sum_lines.decode(fix_encoding))
            print(f"writing {line_counter} lines to fixed width file.")
    print(f"Fixed width file {filename}.txt  has been created with {n_records} records in the output dircetory")