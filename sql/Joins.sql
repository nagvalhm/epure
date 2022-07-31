    -- Joins
    -- Single Left
    
        select * from man 
    left join woman on woman.husband = man.id
    	
--1	nikita	1	klara	1
--2	pasha			
--3	yury	3	natasha	3
   
    
    select * from man
    join woman on true where woman.husband = man.id
    union    
    select man.*, null, null, null from man
    where man.id not in (select husband from woman where husband is not null)
    
 INSERT INTO public.epure_class1(node_id, str2, int2, float2, complex2, list2, tuple2) VALUES ('d487dcc6-056e-474d-ad25-78dc14d60349', \'EpureClass1.str2\', 1488, 3.14, point(3.14, 2.7), \'[1, 2, 3]\', \'{"py/tuple": [1, 2, 3]}\');
    
    
    SELECT table_schema, table_name as table_name, column_name, is_nullable, data_type 
  FROM information_schema.columns where column_name = 'res_id_deleted_d8c4ae0443654deaa3957fc68ba4314e'
    
    
        -- Double Left
    
        select * from man 
    left join woman on woman.husband = man.id
    where man.id > 1
    left join dog on dog.dog_owner = woman.id
    
    
    
    
    
    INSERT INTO public.epure_class1(node_id, str2, int2, 
float2, complex2, list2, tuple2) VALUES 
('414718dd-2672-4852-8be4-4066156659e4', 'EpureClass1.str2', 1488, 3.14, point(3.14, 2.7), '[1, 2, 3]', '{"py/tuple": [1, 2, 3]}');

INSERT INTO public.epure_class2(node_id, epure_class, range2, dict2, 
set2, frozenset2, bool2, bytes2) VALUES 
('3fe41d01-8861-46aa-b28f-e4b6fa231efd', '414718dd-2672-4852-8be4-4066156659e4', 
'{"py/reduce": [{"py/type": "builtins.range"}, {"py/tuple": [0, 10, 1]}]}', 
'{"val1": "val1", "4": 5}', 
'{"py/set": [1, 3, 6]}', 
'{"py/set": [1, 3, 6]}', True, 'epure_class2.bytes');

INSERT INTO public.epure_class3(node_id, epure_class, bytearray2, memoryview2, generic_dict2, generic_list2, lambda_field2) 
VALUES ('92801dea-38a5-4339-bc7d-0f831f460268', 
'3fe41d01-8861-46aa-b28f-e4b6fa231efd', 'epure_class3.bytearray', 
NULL, '{"4": "val1", "val2": 5}', '[1, "2", 3.14]', 'null');

INSERT INTO public.default_epure(node_id, str0, int0, float0, 
complex0, list0, tuple0, range0, dict0, set0, frozenset0, bool0, 
bytes0, bytearray0, memoryview0, generic_dict0, generic_list0, 
generic_tuple0, lambda_field0, str3, int3, float3, complex3, list3, tuple3, 
regular_class, epure_class) 
VALUES ('bfff6fe1-3fd0-4b56-bcd9-1163fbb30c27', 'str0_value', 'uniq_str', 1.4, 
point(5.0, 7.0), NULL, NULL, 
'{"py/reduce": [{"py/type": "builtins.range"}, {"py/tuple": [1, 10, 1]}]}', 
'{"field1": "val1", "field2": 3}', 
'{"py/set": [3, "set_val1", 13.4]}', 
'{"py/reduce": [{"py/type": "builtins.frozenset"}, {"py/tuple": [[1, "2", 3.14]]}]}', 
True, '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\', NULL, NULL, NULL, NULL, NULL, NULL, 
'str3_value', 6, 2.7, NULL, NULL, NULL, 
'{"py/object": "pyt1.tests.epure_classes.RegularClass3", "bytearray1": {"py/object": "builtins.bytearray"}, "NoneType1": "NoneType1", "none1": "none1", "generic_dict1": {"4": "5d", "sdf": 7}, "generic_list1": [4, "dff"]}', 
'92801dea-38a5-4339-bc7d-0f831f460268');
