CREATE table IF NOT EXISTS oraculs_domain.competitions (
    id          SERIAL PRIMARY KEY,    
    data JSONB
);

CREATE table IF NOT EXISTS oraculs_domain.oraculs (
    id          SERIAL PRIMARY KEY,    
    data JSONB
);

CREATE table IF NOT EXISTS oraculs_domain.tasks (
    id          SERIAL PRIMARY KEY,    
    data JSONB
);

GRANT ALL PRIVILEGES ON TABLE oraculs_domain.competitions, 
oraculs_domain.oraculs,
oraculs_domain.tasks
TO oraculs;

    start_date timestamp,
    enter_fee decimal,
    
--insert
insert into oraculs_domain.competitions(data) values 
		(jsonb_build_object('start_date',
			EXTRACT(EPOCH FROM TIMESTAMPTZ '2001-02-16 20:38:40.12-08'),
			'enter_fee',101))
			
insert into oraculs_domain.competitions(data) values 
		(jsonb_build_object('start_date',
			EXTRACT(EPOCH FROM now()),
			'enter_fee',100))

--select
select TO_TIMESTAMP(NULLIF(data->>'start_date', '')::double precision) at time zone '+08' 
as start_date from oraculs_domain.competitions


select TO_TIMESTAMP((EXTRACT(EPOCH FROM TIMESTAMPTZ '2001-02-16 20:38:40.12+08'))) at time zone '+08'

pg_typeof

select TO_TIMESTAMP(id) as start_date from oraculs_domain.competitions

		delete from oraculs_domain.competitions
		
	 

	  SELECT '2018-09-02 07:09:19'::timestamp AT TIME ZONE 'America/Chicago';
	  
	  
select jsonb_build_object('foo',1,'bar',(select extract(epoch from now())))
	  
SELECT TO_TIMESTAMP(
    '2017-03-31 9:30:20',
    'YYYY-MM-DD HH:MI:SS'
);
    
select extract(epoch from now());
 select to_timestamp(extract(epoch from now())); 


select extract(milliseconds from now())
select TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40.12-08'
SELECT EXTRACT(EPOCH FROM TIMESTAMPTZ '2001-02-16 20:38:40.12')
SELECT EXTRACT(EPOCH FROM TIMESTAMP '2001-02-16 20:38:40.12-07')
SELECT EXTRACT(EPOCH FROM TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40.000001-09')

SELECT EXTRACT(EPOCH FROM now()), EXTRACT(EPOCH FROM now()::timestamp)
,  EXTRACT(EPOCH FROM now()::timestamptz)


CREATE TABLE oraculs_domain_entities (
  id          SERIAL PRIMARY KEY, 
  name        TEXT, 
  description TEXT,
  properties  JSONB
);

select * from oraculs_domain_entities

select * from oraculs_domain_entities where properties ->> 'a' like '%ni%'

INSERT INTO oraculs_domain_entities (properties) VALUES 
  ('{}'),
  ('{"a": "nikita"}'),
  ('{"a": 2, "b": ["c", "d"]}'),
  ('{"a": 1, "b": {"c": "d", "e": true}}'),
  ('{"b": 2}');

insert into oraculs_domain_entities values 

    
GRANT ALL PRIVILEGES ON TABLE public.oraculs_domain_entities TO oraculs;

CREATE ROLE odoo SUPERUSER CREATEDB CREATEROLE NOINHERIT LOGIN PASSWORD 'odoo';


