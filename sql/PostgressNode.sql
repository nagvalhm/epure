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
  
  select * from separated_epure1
  
  
  
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
   
   select * from rak_occurrence
   
   CREATE TABLE public.rak_occurrence (
	id serial NOT NULL,
	"name" varchar NOT NULL,
	email_text text NULL,
	"language" int4 NULL,
	"comment" text NULL,
	state int4 NULL,
	insurance_type int4 NULL,
	supervisors int4 NULL,
	executers int4 NULL,
	executer int4 NULL,
	"operator" int4 NULL,
	claimant_state int4 NULL,
	create_uid int4 NULL,
	create_date timestamp NULL,
	write_uid int4 NULL,
	write_date timestamp NULL,
	is_valid bool NULL,
	assignment_time timestamp NULL,
	CONSTRAINT rak_occurrence_pkey PRIMARY KEY (id)
);


-- public.rak_occurrence foreign keys

ALTER TABLE public.rak_occurrence ADD CONSTRAINT rak_occurrence_claimant_state_fkey FOREIGN KEY (claimant_state) REFERENCES rak_claimant_state(id) ON DELETE SET NULL;
ALTER TABLE public.rak_occurrence ADD CONSTRAINT rak_occurrence_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;
ALTER TABLE public.rak_occurrence ADD CONSTRAINT rak_occurrence_executer_fkey FOREIGN KEY (executer) REFERENCES res_users(id) ON DELETE SET NULL;
ALTER TABLE public.rak_occurrence ADD CONSTRAINT rak_occurrence_executers_fkey FOREIGN KEY (executers) REFERENCES res_groups(id) ON DELETE SET NULL;
ALTER TABLE public.rak_occurrence ADD CONSTRAINT rak_occurrence_language_fkey FOREIGN KEY (language) REFERENCES res_lang(id) ON DELETE SET NULL;
ALTER TABLE public.rak_occurrence ADD CONSTRAINT rak_occurrence_operator_fkey FOREIGN KEY (operator) REFERENCES res_users(id) ON DELETE SET NULL;
ALTER TABLE public.rak_occurrence ADD CONSTRAINT rak_occurrence_state_fkey FOREIGN KEY (state) REFERENCES rak_occurrence_state(id) ON DELETE SET NULL;
ALTER TABLE public.rak_occurrence ADD CONSTRAINT rak_occurrence_supervisors_fkey FOREIGN KEY (supervisors) REFERENCES res_groups(id) ON DELETE SET NULL;
ALTER TABLE public.rak_occurrence ADD CONSTRAINT rak_occurrence_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;