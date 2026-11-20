CREATE TABLE Data_Layers (
	 LayerID SERIAL PRIMARY KEY,
	 LayerName VARCHAR(50) UNIQUE NOT NULL,
	 Description TEXT
);

INSERT INTO Data_Layers (LayerName, Description)
VALUES 
	('Bronze', 'Bronze layer of the medal'), 
	('Silver', 'Silver layer of the medal'), 
	('Gold', 'Gold layer of the medal');

ALTER TABLE Data_Layers 
ADD COLUMN manager_email VARCHAR(100);

UPDATE Data_Layers
SET manager_email = 'bronze@gmail.com'
WHERE LayerID = 1;

UPDATE Data_Layers
SET manager_email = 'silver@gmail.com'
WHERE LayerID = 2;

UPDATE Data_Layers
SET manager_email = 'gold@gmail.com'
WHERE LayerID = 3;

ALTER TABLE Data_Layers 
ADD UNIQUE (manager_email);

ALTER TABLE shops
RENAME COLUMN address TO shop_address;