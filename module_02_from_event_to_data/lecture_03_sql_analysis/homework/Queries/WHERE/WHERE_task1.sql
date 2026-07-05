SELECT 
	sh.shop_id,
	sh.address AS shop_address,
	ci.city_name,
	co.country_name
FROM 
	shops sh
JOIN cities ci ON sh.city_id = ci.city_id
JOIN countries co ON ci.country_id = co.country_id
WHERE country_name = 'Poland';