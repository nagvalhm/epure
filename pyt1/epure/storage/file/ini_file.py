from configparser import ConfigParser
from .file_storage import FileStorage
from typing import Any, Dict
from io import StringIO

class IniSection:
    pass

class IniFile(FileStorage):

    parser: ConfigParser


    def __init__(self, path:str):

        parser = self.parser = ConfigParser()
        with open(path, 'r') as file:
            config_string = '[NONE_SECTION]\n' + file.read()            
            parser.read_string(config_string)

        if dict(parser['NONE_SECTION']):
            self.__dict__ |= dict(parser['NONE_SECTION'])

        for section in parser:
            section_val = parser[section]
            if section == 'NONE_SECTION':
                continue
            nesting = section.split('.')
            is_nested = len(nesting) > 1
            if is_nested:
                self._get_nested_dict(nesting, section_val)
                continue
            self.__dict__[section] = self._get_ini_section(section_val)
            # dict(parser[section])
        
        return super().__init__(path)

    def _get_ini_section(self, section_val:Any) -> object:
        obj = IniSection()
        obj.__dict__ = dict(section_val)
        return obj

    def _get_nested_dict(self, nesting:Any, section_val:Any) -> None:
        res: Any = self._get_ini_section(section_val)
        for sec in reversed(nesting):
            res = {sec : self._get_ini_section(res) }
        self.__dict__ |= res


    # def save(self) -> Any:
    #     output = StringIO()
    #     self.parser.write(output)
    #     res = output.getvalue().split('\n', 1)[2]
    #     with open(self.path, 'w') as configfile:
    #         configfile.write(res)        