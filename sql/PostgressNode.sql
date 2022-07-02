CREATE TABLE test_cls (
	test_field1 text,  
	test_field2 text,  
	test_field3 json,  
	test_field4 bytea,  
	test_field5 text 
); 

CREATE TABLE oraculs_domain.test_clssasdas (
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
  
  
  
  
  
  select data_type from information_schema.columns group by data_type
  
 select column_name, table_schema || '.' || table_name as table_name
 from information_schema.columns where  data_type = 'timestamp with time zone'
 
 select created from information_schema.routines where created is not null
 
  select count(*) from information_schema.columns where table_name = 'columns'
 
 select cast(4294967295 as decimal)
 
 select cast(-1 as oid)
 
 ({CONST :consttype 3802 :consttypmod -1 :constcollid 0 :constlen -1 :constbyval false :constisnull false :location 94 :constvalue 8 [ 32 0 0 0 0 0 0 32 ]} {CONST :consttype 16 :consttypmod -1 :constcollid 0 :constlen 1 :constbyval true :constisnull false :location 142 :constvalue 1 [ 0 0 0 0 0 0 0 0 ]})
 
 SELECT count(1) FROM pg_catalog.pg_tables as tbl

  
 select authorization_identifier from information_schema._pg_foreign_data_wrappers
  
  WHERE table_schema = 'oraculs_domain'
   AND table_name   = 'your_table'