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

select * from information_schema.columns
SELECT con.*
       FROM pg_catalog.pg_constraint con
       
       select * from default_epure
       
alter table separated_epure1 add column temp_col3 integer UNIQUE
ALTER TABLE public.separated_epure1 DROP COLUMN temp_col;

INSERT INTO public.separated_epure1
(str2, int1, float1_deleted155375a36f4b42c896c08735b4bdcdb6, complex1_deleted0df13057ba7c496e819bf08bf5f01410, list1, tuple1, str1, float1, complex1)
VALUES('val', 6, 5, '{34.5,103.4}', NULL, NULL, NULL, NULL, NULL);





select * from information_schema.tables where table_name like '%test%'

SELECT * FROM pg_catalog.pg_tables as tbl
where tablename like '%information_schema%'
left join information_schema.columns


SELECT table_schema, table_name as table_name, column_name, is_nullable, data_type 
  FROM information_schema.columns where table_name = 'separated_epure1'
  order by table_schema, table_name
  
  select * from 
  information_schema.columns col
  left join information_schema.constraint_column_usage
  

  
  where col.table_name = 'default_epure'
  
  
    select * from information_schema.columns where table_name like '%information_schema%'
      select * from  information_schema.table_constraints
      select * from  information_schema.constraint_column_usage
  
 select * from  information_schema.KEY_COLUMN_USAGE
  
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
   
   
   INSERT INTO public.separated_epure1
(str1, int1, float1, complex1)
VALUES('val', 6, 4.8, array[34.5, 103.4]);

ALTER TABLE public.separated_epure1 ALTER COLUMN str1 TYPE integer;

--epure_deleted_columns
--CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
--
--create sequence if not exists temp_seq;


ALTER TABLE public.separated_epure1  RENAME COLUMN str2 to sdfsdf;

--select gen_random_uuid()

ALTER TABLE public.separated_epure1 ALTER COLUMN str2 SET NOT NULL;

UPDATE public.separated_epure1 SET str2 = str5;


select gen_random_uuid ()


CREATE TABLE public.separated_epure1 (
	str1 text NULL,
	int1 int8 NULL,
	float1 numeric NULL,
	complex1 _numeric NULL,
	list1 jsonb NULL,
	tuple1 jsonb NULL
);
   
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

select * from public.default_epure


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




----
  SELECT cols.table_schema, cols.table_name, 
                    cols.column_name, cols.is_nullable, cols.data_type, cols.column_default,
				    cols_constr.table_schema AS foreign_schema,
				    cols_constr.table_name AS foreign_table,
				    cols_constr.column_name AS foreign_column,
                    constr.constraint_type
                    FROM information_schema.columns cols
                    left join information_schema.constraint_column_usage cols_constr
                    	on cols.table_schema = cols_constr.table_schema and cols.table_name = cols_constr.table_name
                    	and cols.column_name = cols_constr.column_name
                    left join information_schema.table_constraints constr
                    	on cols_constr.constraint_name = constr.constraint_name
                    
                    where constr.constraint_type = 'FOREIGN KEY'
                    
                    where cols_constr.column_name is not null
                    where cols.table_schema = 'public' and cols.table_name = 'default_epure'
                    	
                    ORDER BY cols.table_schema, cols.table_name
                    
                    point((5.0)::double precision, (7.0)::double precision)
                    
                    
      select * from information_schema.columns where column_default is not null
      
select * from default_epure de 



          SELECT cols.table_schema, cols.table_name, 
                    cols.column_name, cols.is_nullable, cols.data_type, cols.column_default,
                    cols_constr.table_schema AS foreign_schema,
				    cols_constr.table_name AS foreign_table,
				    cols_constr.column_name AS foreign_column,
                    constr.constraint_type
                    FROM information_schema.columns cols
                    left join information_schema.constraint_column_usage cols_constr
                    	on cols.table_schema = cols_constr.table_schema and cols.table_name = cols_constr.table_name
                    	and cols.column_name = cols_constr.column_name
                    left join information_schema.constraint_column_usage cols_constr
                    	on cols.table_schema = cols_constr.table_schema and cols.table_name = cols_constr.table_name
                    	and cols.column_name = cols_constr.column_name
                    left join information_schema.table_constraints constr
                    	on cols_constr.constraint_name = constr.constraint_name
                    ORDER BY cols.table_schema, cols.table_name
                    
                    
       SELECT * FROM public.default_epure
        full JOIN oraculs_domain.test_clssasdas
        ON (public.default_epure.str0 = oraculs_domain.test_clssasdas.test_field1)
        where 
        public.default_epure.str3 = oraculs_domain.test_clssasdas.test_field2 
        
        create table man (
        	id integer,
        	man_name text
        
        );
       
       insert into man (id, man_name) values (1, 'nikita');
      insert into man (id, man_name) values (2, 'pasha');
     	insert into man (id, man_name) values (3, 'yury');
       
        create table woman (
        	id integer,
        	woman_name text,
        	husband integer
        );
       
   insert into woman (id, woman_name, husband) values (1, 'klara', 1);
      insert into woman (id, woman_name) values (2, 'dasha');
     	insert into woman (id, woman_name, husband) values (3, 'natasha', 3);
       
        create table dog (
        	id integer,
        	dog_name text,
        	dog_owner integer
        );

   insert into dog (id, dog_name) values (1, 'elli');
      insert into dog (id, dog_name, dog_owner) values (2, 'dog', 2);
     	insert into dog (id, dog_name, dog_owner) values (3, 'kotya', 3);
     	
     
	select * from dog
    
    select woman.*, woman.husband, dog.dog_name from woman
    left join dog on dog.dog_owner < woman.id
    
    
        select woman.* from woman
    left join dog on dog.dog_owner < woman.id 

    
    SELECT public.default_epure.*, oraculs_domain.test_clssasdas.* FROM public.default_epure  LEFT JOIN oraculs_domain.test_clssasdas on str0 == test_field1 WHERE  (((int0 = test_field2)   and (float0 = 5)) or (complex0 = test_field3))
    
    select * from default_epure
    
    
    select * from man 
    join woman on woman.husband = man.id
    union (select man.*, null, null, null from man except )
    
    
     select * from man
--     (select * from man union select null, null) man
    full outer join (select * from woman union select null, null, null) woman on true
--    full join (select * from dog union select null, null, null) dog on true
--     where (man.id is not null)
    where (man.id is not null and (woman.husband = man.id or woman.husband is null))
    
    and dog.dog_owner = woman.id