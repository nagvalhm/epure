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
    
 
    
    
    
    
    
        -- Double Left
    
        select * from man 
    left join woman on woman.husband = man.id
    where man.id > 1
    left join dog on dog.dog_owner = woman.id
