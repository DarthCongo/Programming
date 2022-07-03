/* Query 1 - Most popular actor based on rental  */


WITH t1 as ( 
	     SELECT f.length, 
	            COUNT(r.*) rental_count,
             CASE WHEN f.length < 60 THEN '1 hr or less'
	          WHEN f.length >= 60 AND f.length <= 120 THEN 'Between 1-2 hrs'
                  WHEN f.length >= 120 AND f.length <= 180 THEN 'Between 2-3 hrs'
	          ELSE 'More than 3 hrs' 
             END AS filmlen_groups
             FROM film_actor fa
             JOIN   actor a ON fa.actor_id = a.actor_id
             JOIN film f ON f.film_id = fa.film_id
             JOIN inventory i ON f.film_id = i.film_id
             JOIN rental r ON r.inventory_id = i.inventory_id
             GROUP BY 1
             ORDER BY 2 DESC 
           ),
    t2 AS  ( 
             SELECT filmlen_groups,
	            SUM(rental_count) total_rental
	     FROM t1
	     GROUP BY 1
           )
SELECT filmlen_groups,
       ROUND(total_rental / (SELECT sum(total_rental)FROM t2) * 100,2) AS percent_rental
FROM t2
ORDER BY 2 DESC



/* Query 2 What movie categories are popular in each day of the week? */
-----------------------------------------------------------------------------------------------------------------------------

WITH t1 AS ( 
             SELECT DISTINCT(name) AS category_name,
		    DATE_PART('dow',rental_date) AS day_of_week,
		    COUNT(r.*) OVER (PARTITION BY name ORDER BY date_part('dow',rental_date)) AS rental_count
	     FROM rental r
	     JOIN inventory i ON r.inventory_id = i.inventory_id
	     JOIN film f ON f.film_id = i.film_id
	     JOIN film_category fc ON fc.film_id = f.film_id
	     JOIN category c ON c.category_id = fc.category_id
	     ORDER BY 2, 3 DESC
           ),
     t2 AS ( 
             SELECT t1.*,
	    	    SUM(rental_count) OVER (PARTITION BY day_of_week) AS total_per_day
	     FROM t1
           ),
     t3 as (
             SELECT category_name,
                    CASE WHEN day_of_week = 0 THEN ROUND((rental_count / total_per_day) * 100,2) END AS sun,
	            CASE WHEN day_of_week = 1 THEN ROUND((rental_count / total_per_day) * 100,2) END AS mon,
	            CASE WHEN day_of_week = 2 THEN ROUND((rental_count / total_per_day) * 100,2) END AS tue,
                    CASE WHEN day_of_week = 3 THEN ROUND((rental_count / total_per_day) * 100,2) END AS wed,
	            CASE WHEN day_of_week = 4 THEN ROUND((rental_count / total_per_day) * 100,2) END AS thu,
	            CASE WHEN day_of_week = 5 THEN ROUND((rental_count / total_per_day) * 100,2) END AS fri,
	            CASE WHEN day_of_week = 6 THEN ROUND((rental_count / total_per_day) * 100,2) END AS sat	   
             FROM t2 
           ),
     t4 AS (
             SELECT category_name, sun 
             FROM t3
           ),
     t5 AS ( 
             SELECT category_name, mon
             FROM t3
           ),
     t6 AS (
             SELECT category_name, tue
             FROM t3
           ),
     t7 AS (
             SELECT category_name, wed
             FROM t3
           ),
     t8 AS (
             SELECT category_name, thu
             FROM t3
           ),
     t9 AS (
             SELECT category_name, fri
             FROM t3
           ),
    t10 AS (
             SELECT category_name, sat
             FROM t3
           )

SELECT t4.category_name, mon, tue, wed, thu, fri, sat, sun 
FROM t4 
JOIN t5 ON t4.category_name = t5.category_name AND sun is not null
JOIN t6 ON t5.category_name = t6.category_name AND mon is not null
JOIN t7 ON t6.category_name = t7.category_name AND tue is not null
JOIN t8 ON t7.category_name = t8.category_name AND wed is not null
JOIN t9 ON t8.category_name = t9.category_name AND thu is not null
JOIN t10 ON t9.category_name = t10.category_name AND fri is not null and sat is not null




/* Query 3 What makes up the percentage of revenue of each store based by movie ratings. */


WITH t1 AS ( 
             SELECT st.store_id,
	            rating,
		    COUNT(rental_date),
		    SUM(amount) AS store_one
             FROM film f
	     JOIN inventory i ON f.film_id = i.film_id
	     JOIN rental r ON r.inventory_id = i.inventory_id
 	     JOIN payment p ON p.rental_id = r.rental_id
	     JOIN staff s ON p.staff_id = s.staff_id
	     JOIN store st ON st.store_id = s.store_id
	     AND st.store_id = 1
             GROUP BY 1,2
           ),
     t2 AS ( 
              SELECT st.store_id,
                     rating,
		     COUNT(rental_date),
		     SUM(amount) AS store_two
	      FROM film f
	      JOIN inventory i ON f.film_id = i.film_id
     	      JOIN rental r ON r.inventory_id = i.inventory_id
	      JOIN payment p ON p.rental_id = r.rental_id
	      JOIN staff s ON p.staff_id = s.staff_id
	      JOIN store st ON st.store_id = s.store_id
	      AND st.store_id = 2
	      GROUP BY 1,2
            ), 
      t3 AS ( 
               SELECT t1.rating,
	 	      CASE WHEN t1.store_id = 1 THEN t1.store_one END AS store_one,
		      SUM(store_one) OVER () AS total_store_one,
		      CASE WHEN t2.store_id = 2 THEN t2.store_two END AS store_two,
	              SUM(store_two) OVER () AS total_store_two
	       FROM t1
	       JOIN t2 ON t1.rating = t2.rating
            )

SELECT rating,
       ROUND((store_one / total_store_one) * 100,2) store_one_percent_revenue,
       ROUND((store_two / total_store_two) * 100,2) store_two_percent_revenue
FROM t3




/* Query 4 Get customer count, average spend, and total spend. Limited to top 10 countries that spent the most. */ 


WITH t1 AS ( 
             SELECT DISTINCT(cr.country) AS country,
		    COUNT(c.customer_id) OVER (PARTITION BY cr.country) AS customer_count
	     FROM customer c
	     JOIN address a ON c.address_id = a.address_id
	     JOIN city ct ON ct.city_id = a.city_id
	     JOIN country cr ON ct.country_id = cr.country_id
	   ),
     t2 AS ( 
             SELECT DISTINCT(country) AS country,
	            AVG(amount) OVER (PARTITION BY country) avg_spend,
	            SUM(amount) OVER (PARTITION BY country) total_spend
	     FROM country cr
	     JOIN city ct ON cr.country_id = ct.country_id
	     JOIN address a ON a.city_id = ct.city_id
	     JOIN customer c ON c.address_id = a.address_id
	     JOIN payment p ON p.customer_id = c.customer_id
	   )
SELECT t2.country AS country,
       t1.customer_count AS customer_count,
       ROUND(t2.avg_spend,2) AS avg_spend,
       t2.total_spend AS total_spend
FROM t2
JOIN t1 ON t1.country = t2.country
ORDER BY 4 DESC
LIMIT 10

