-- 1. Top-selling food items

SELECT f.name,
       SUM(o.quantity) AS total_sold
FROM food_items f
JOIN orders o
ON f.food_id = o.food_id
GROUP BY f.food_id, f.name
ORDER BY total_sold DESC;


-- 2. Total revenue

SELECT SUM(total_amount) AS total_revenue
FROM orders
WHERE status != 'Cancelled';


-- 3. Customers with more than 3 orders

SELECT c.name,
       COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 3;


-- 4. Most popular restaurant

SELECT r.name,
       COUNT(o.order_id) AS total_orders
FROM restaurants r
JOIN food_items f
ON r.restaurant_id = f.restaurant_id
JOIN orders o
ON f.food_id = o.food_id
GROUP BY r.restaurant_id, r.name
ORDER BY total_orders DESC;


-- 5. Daily order report

SELECT DATE('now') AS report_date,
       COUNT(*) AS total_orders,
       SUM(total_amount) AS revenue
FROM orders;


-- 6. Rank food items by sales

SELECT
    food_name,
    total_sales,
    RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM (
    SELECT
        f.name AS food_name,
        SUM(o.quantity) AS total_sales
    FROM food_items f
    JOIN orders o
    ON f.food_id = o.food_id
    GROUP BY f.food_id, f.name
) ranked_foods;
