class EpureError(Exception):
    pass

class DbError(Exception):
    pass

class DefaultConstraintError(AttributeError):
    def get_message(self, class_name:str, field_name:str):
        return f'''field {field_name} of {class_name} doesn't have default value.
            Default type constraint (etc Default, NotNull, Id)
                            must be provided with default value:
                            @epure()
                            class MyClass:
                                my_id:Id[int] = 0
                                ...
                            '''

    def __init__(self, class_name:str='', field_name:str='', message:str=''):
            if message:
                self.message = message
            else:
                self.message = self.get_message(class_name, field_name)
            super().__init__(self.message)