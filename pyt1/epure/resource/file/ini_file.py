from configparser import ConfigParser, RawConfigParser
from .file_storage import FileStorage
from typing import Any
from io import StringIO
from .ini_section import ActualIniSection, NoneIniSection


class IniFile(FileStorage):

    parser: RawConfigParser
    virtual_section: ActualIniSection

    def __init__(self, path:str):

        parser = self.parser = ConfigParser()
        with open(path, 'r') as file:
            config_string = '[VIRTUAL_SECTION]\n' + file.read()            
            parser.read_string(config_string)
        self.virtual_section = ActualIniSection(parser, 'VIRTUAL_SECTION')

        
    def __getattr__(self, attr_name: str) -> Any:
        if attr_name in self.virtual_section:
            return self.virtual_section.__getattr__(attr_name)
        elif attr_name in self.parser:
            return ActualIniSection(self.parser, attr_name)
        else:
            return NoneIniSection(self.parser, attr_name)

    # def save(self) -> Any:
    #     output = StringIO()
    #     self.parser.write(output)
    #     res = output.getvalue().split('\n', 1)[2]
    #     with open(self.path, 'w') as configfile:
    #         configfile.write(res)