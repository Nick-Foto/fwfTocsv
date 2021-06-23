import re

class spec_class:
    def __init__(self, spec_filename: str):
        try:
            with open(spec_filename) as specfile:
                str_spec = specfile.read()    
        except:
            print('spec file not found!')
            return None
    
        str_spec=str_spec.replace('\n',' ')
        try :

            name_pattern = r'columnnames"(.*)"offsets'
            names = re.findall(name_pattern , str_spec, re.I)[0]

            column_pattern= r'"?(\w+)"?'
            column_names = re.findall(column_pattern , names, re.I)

            offsets_string = re.findall(r'offsets"(.*)"fixed', str_spec, re.I)[0]
            offsets = re.findall(r'"?(\d+)"?', offsets_string, re.I)
            offsets= [*map(int,offsets)]

            encoding_pattern = r'fixedwidthencoding"\s*:?\s*"?([a-z0-9,-]+)"?.*'
            FixedWidthEncoding = re.findall(encoding_pattern , str_spec, re.I)[0]

            inch_pattern = r'includeheader"\s*:?\s*"?([0-9a-z,-]+)"?.*'
            IncludeHeader = re.findall(inch_pattern , str_spec, re.I)[0]
            IncludeHeader = True if IncludeHeader.lower() == 'true' else False
    
            encoding_pattern2 = r'delimitedencoding"\s*:?\s*"?([a-z0-9,-]+)"'
            DelimitedEncoding= re.findall(encoding_pattern2 , str_spec, re.I)[0]
        except:
            print('Bad format in spec file')
            return None

        self.columns = tuple(zip(column_names,offsets))
        self.fixedwidth_encoding=FixedWidthEncoding
        self.include_header=IncludeHeader
        self.delimited_encoding=DelimitedEncoding

        
