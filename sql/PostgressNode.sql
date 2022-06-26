CREATE TABLE test_cls (
	test_field1 text,  
	test_field2 text,  
	test_field3 json,  
	test_field4 bytea,  
	test_field5 text 
); 

CREATE TABLE test_clssasdas (
test_field1 text,  
test_field2 text,  
test_field3 json,  
test_field4 bytea,  
test_field5 text
); 

CREATE TABLE public.oraculs_domai (
	test_field1 text,  
test_field2 text,  
test_field3 json,  
test_field4 bytea,  
test_field5 text
	
);

select * from information_schema.tables where table_name like '%test%'