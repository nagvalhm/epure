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
    
    
    
    
    
        -- Double Left
    
        select * from man 
    left join woman on woman.husband = man.id
    where man.id > 1
    left join dog on dog.dog_owner = woman.id
