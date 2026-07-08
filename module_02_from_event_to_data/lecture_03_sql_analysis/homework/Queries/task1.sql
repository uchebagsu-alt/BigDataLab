INSERT INTO products (product_id, product_name, price, category_id, class, modify_timestamp, resistant, is_allergic, vitality_days)
VALUES 
	(9991, 'Organic Dragon Fruit', 15.99, 1, 'A', '2023-10-01 10:00:00', 'Yes', 'Yes', 14),
	(9992, 'Gluten Free Oat Cookies', 8.50, 2, 'B', '2023-10-01 10:05:00', 'No', 'Yes', 60);

SELECT * FROM products
WHERE  is_allergic = 'Yes' and resistant = 'Yes';

UPDATE products SET is_allergic = 'Yes'
WHERE product_name = 'Bananas Family Pack';

DELETE FROM products
WHERE product_id = 9991 and product_name = 'Organic Dragon Fruit';

SELECT * FROM Products;