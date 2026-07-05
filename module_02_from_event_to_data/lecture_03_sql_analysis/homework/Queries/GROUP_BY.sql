SELECT 
	co.country_name,
	COUNT(sh.shop_id) AS shop_count
FROM 
	shops sh
JOIN cities ci ON sh.city_id = ci.city_id
JOIN countries co ON ci.country_id = co.country_id
GROUP BY co.country_name
ORDER BY shop_count DESC;