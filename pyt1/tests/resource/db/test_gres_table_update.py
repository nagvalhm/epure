from ....epure.epure import Epure, epure, connect

#columns
def test_create_column():
    pass

def test_update_column_type():
    pass

def test_delete_column():
    pass

#constrains
def test_update_table_constrains():
    pass

#data
def test_create_row():
    pass

def test_update_row():
    pass

def test_restore_column():

    @epure()
    class EpureRestoreColumn:
        str2:str = 'EpureClass1.str2'

        int2:int


    instance1 = EpureRestoreColumn()
    res = instance1.execute('''SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'public' AND 
        TABLE_NAME = 'epure_restore_column' AND COLUMN_NAME  = 'int2' ''')[0][0]
    assert res == 'bigint'

    @epure()
    class EpureRestoreColumn:
        str2:str = 'EpureClass1.str2'

        int2:str

    instance2 = EpureRestoreColumn()
    res = instance2.execute('''SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'public' AND 
        TABLE_NAME = 'epure_restore_column' AND COLUMN_NAME  = 'int2' ''')[0][0]
    assert res == 'text'

    @epure()
    class EpureRestoreColumn:
        str2:str = 'EpureClass1.str2'

        int2:int

    instance3 = EpureRestoreColumn()

    res = instance3.execute('''SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'public' AND 
        TABLE_NAME = 'epure_restore_column' AND COLUMN_NAME  = 'int2' ''')[0][0]
    assert res == 'bigint'