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

SELECT * FROM pg_catalog.pg_tables as tbl
where tablename like '%information_schema%'
left join information_schema.columns


SELECT table_schema, table_name as table_name, column_name, is_nullable, data_type 
  FROM information_schema.columns order by table_schema, table_name
  
 select authorization_identifier from information_schema._pg_foreign_data_wrappers
  
  WHERE table_schema = 'oraculs_domain'
   AND table_name   = 'your_table'