CREATE TABLE oraculs_tecnical.nodes (
    id     INT GENERATED ALWAYS AS IDENTITY,
    parent INT,
    node_name   VARCHAR(255) NOT null,
    node_type   INT,
    node_state  INT,
    CONSTRAINT "oraculs_tecnical.nodes_pk" PRIMARY KEY (id)
--     CONSTRAINT fk_type 
-- FOREIGN KEY(type) 
-- 	  REFERENCES node_types(id)
); 
commit;

DELETE FROM public.flyway_schema_history
WHERE installed_rank=3;


grant usage, create on schema oraculs_tecnical to oraculs;
grant usage, create on schema oraculs_domain to oraculs;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA oraculs_tecnical TO oraculs;
ALTER DEFAULT PRIVILEGES IN SCHEMA oraculs_domain GRANT UPDATE, INSERT, SELECT, DELETE ON TABLES TO oraculs;

delete from flyway_schema_history 

DELETE FROM public.flyway_schema_history
WHERE installed_rank=2;
 

select * from oraculs_tecnical.nodes

select * from public.flyway_schema_history

GRANT ALL PRIVILEGES ON TABLE public.flyway_schema_history TO oraculs;

DELETE FROM public.flyway_schema_history
WHERE installed_rank=4;

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
