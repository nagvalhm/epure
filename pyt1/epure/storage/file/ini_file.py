from configparser import ConfigParser, RawConfigParser
from .file_storage import FileStorage
from typing import Any
from io import StringIO
from .ini_section import IniSection, NoneIniSection


class IniFile(FileStorage):

    parser: RawConfigParser
    virtual_section: IniSection

    def __init__(self, path:str):

        parser = self.parser = ConfigParser()
        with open(path, 'r') as file:
            config_string = '[VIRTUAL_SECTION]\n' + file.read()            
            parser.read_string(config_string)
        self.virtual_section = IniSection(parser, 'VIRTUAL_SECTION')

        
    def __getattr__(self, attr_name: str) -> Any:
        if attr_name in self.virtual_section:
            return self.virtual_section.__getattr__(attr_name)
        elif attr_name in self.parser:
            return IniSection(self.parser, attr_name)
        else:
            return NoneIniSection(self.parser, attr_name)

    # def save(self) -> Any:
    #     output = StringIO()
    #     self.parser.write(output)
    #     res = output.getvalue().split('\n', 1)[2]
    #     with open(self.path, 'w') as configfile:
    #         configfile.write(res)        


    #     if dict(parser['NONE_SECTION']):
    #         self.__dict__ |= dict(parser['NONE_SECTION'])

    #     for section in parser:
    #         section_val = parser[section]
    #         if section == 'NONE_SECTION':
    #             continue
    #         nesting = section.split('.')
    #         is_nested = len(nesting) > 1
    #         if is_nested:
    #             self._get_nested_dict(nesting, section_val)
    #             continue
    #         self.__dict__[section] = self._get_ini_section(section_val)
    #         # dict(parser[section])
        
    #     return super().__init__(path)

    # def _get_ini_section(self, section_val:Any) -> object:
    #     obj = IniSection()
    #     obj.__dict__ = dict(section_val)
    #     return obj

    # def _get_nested_dict(self, nesting:Any, section_val:Any) -> None:
    #     res: Any = self._get_ini_section(section_val)
    #     for sec in reversed(nesting):
    #         res = {sec : self._get_ini_section(res) }
    #     self.__dict__ |= res