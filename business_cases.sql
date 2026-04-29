-- ================================================
-- PhonePe Business Case Study - SQL Queries
-- Author: Sabitha
-- Date: April 2026
-- ================================================

USE phonepe_pulse;

-- ================================================
-- CASE 1: Decoding Transaction Dynamics
-- ================================================
USE phonepe_pulse;

-- 1a. Total transaction amount and count by state (Top 10)
SELECT state, 
       SUM(transaction_count) AS total_transactions,
       ROUND(SUM(transaction_amount)/1000000, 2) AS total_amount_millions
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount_millions DESC
LIMIT 10;

-- 1b. Transaction trend by year and quarter
SELECT year, quarter,
       SUM(transaction_count) AS total_transactions,
       ROUND(SUM(transaction_amount)/1000000, 2) AS total_amount_millions
FROM aggregated_transaction
GROUP BY year, quarter
ORDER BY year, quarter;

-- 1c. Most popular transaction type overall
SELECT transaction_type,
       SUM(transaction_count) AS total_count,
       ROUND(SUM(transaction_amount)/1000000, 2) AS total_amount_millions
FROM aggregated_transaction
GROUP BY transaction_type
ORDER BY total_count DESC;

-- 1d. States with declining transactions (2022 vs 2023)
SELECT state,
       SUM(CASE WHEN year = 2022 THEN transaction_amount ELSE 0 END) AS amt_2022,
       SUM(CASE WHEN year = 2023 THEN transaction_amount ELSE 0 END) AS amt_2023,
       ROUND((SUM(CASE WHEN year = 2023 THEN transaction_amount ELSE 0 END) -
              SUM(CASE WHEN year = 2022 THEN transaction_amount ELSE 0 END))
              / NULLIF(SUM(CASE WHEN year = 2022 THEN transaction_amount ELSE 0 END), 0) * 100, 2) 
              AS growth_percentage
FROM aggregated_transaction
GROUP BY state
ORDER BY growth_percentage ASC
LIMIT 10;

-- ================================================
-- CASE 2: Device Dominance & User Engagement
-- ================================================

-- 2a. Top 10 device brands by total registered users
SELECT brand,
       SUM(user_count) AS total_users,
       ROUND(AVG(user_percentage), 2) AS avg_percentage
FROM aggregated_user
GROUP BY brand
ORDER BY total_users DESC
LIMIT 10;

-- 2b. Brand dominance by state (which brand leads each state)
SELECT state, brand, SUM(user_count) AS total_users
FROM aggregated_user
GROUP BY state, brand
ORDER BY state, total_users DESC;

-- 2c. States where app engagement is low despite high registrations
SELECT state,
       SUM(registered_users) AS total_registered,
       SUM(app_opens) AS total_app_opens,
       ROUND(SUM(app_opens) / NULLIF(SUM(registered_users), 0), 2) AS engagement_ratio
FROM map_user
GROUP BY state
ORDER BY engagement_ratio ASC
LIMIT 10;

-- ================================================
-- CASE 4: Transaction Analysis for Market Expansion
-- ================================================

-- 4a. Top 10 states by transaction volume
SELECT state,
       SUM(transaction_count) AS total_transactions,
       ROUND(SUM(transaction_amount)/10000000, 2) AS total_amount_crores
FROM map_transaction
GROUP BY state
ORDER BY total_transactions DESC
LIMIT 10;

-- 4b. Bottom 10 states (low penetration = expansion opportunity)
SELECT state,
       SUM(transaction_count) AS total_transactions,
       ROUND(SUM(transaction_amount)/10000000, 2) AS total_amount_crores
FROM map_transaction
GROUP BY state
ORDER BY total_transactions ASC
LIMIT 10;

-- 4c. Quarter-wise growth trend per state
SELECT state, year, quarter,
       SUM(transaction_count) AS total_transactions,
       ROUND(SUM(transaction_amount)/1000000, 2) AS amount_millions
FROM map_transaction
GROUP BY state, year, quarter
ORDER BY state, year, quarter;

-- 4d. Top 10 districts by transaction amount
SELECT state, district,
       SUM(transaction_count) AS total_transactions,
       ROUND(SUM(transaction_amount)/1000000, 2) AS amount_millions
FROM map_transaction
GROUP BY state, district
ORDER BY amount_millions DESC
LIMIT 10;

-- ================================================
-- CASE 5: User Engagement & Growth Strategy
-- ================================================

-- 5a. Top 10 states by registered users
SELECT state,
       SUM(registered_users) AS total_registered_users,
       SUM(app_opens) AS total_app_opens
FROM map_user
GROUP BY state
ORDER BY total_registered_users DESC
LIMIT 10;

-- 5b. User growth year over year
SELECT year,
       SUM(registered_users) AS total_users,
       SUM(app_opens) AS total_app_opens
FROM map_user
GROUP BY year
ORDER BY year;

-- 5c. Top 10 districts with highest user engagement
SELECT state, district,
       SUM(registered_users) AS registered_users,
       SUM(app_opens) AS app_opens,
       ROUND(SUM(app_opens) / NULLIF(SUM(registered_users), 0), 2) AS engagement_ratio
FROM map_user
GROUP BY state, district
ORDER BY engagement_ratio DESC
LIMIT 10;

-- 5d. Bottom 10 districts (growth opportunity)
SELECT state, district,
       SUM(registered_users) AS registered_users,
       SUM(app_opens) AS app_opens
FROM map_user
GROUP BY state, district
ORDER BY registered_users ASC
LIMIT 10;

-- ================================================
-- CASE 7: Transaction Analysis Across States & Districts
-- ================================================

-- 7a. Top 10 states overall
SELECT state,
       SUM(transaction_count) AS total_count,
       ROUND(SUM(transaction_amount)/10000000, 2) AS total_crores
FROM top_transaction
GROUP BY state
ORDER BY total_crores DESC
LIMIT 10;

-- 7b. Top 10 districts overall
SELECT state, entity_name AS district,
       SUM(transaction_count) AS total_count,
       ROUND(SUM(transaction_amount)/10000000, 2) AS total_crores
FROM top_transaction
WHERE entity_type = 'districts'
GROUP BY state, entity_name
ORDER BY total_crores DESC
LIMIT 10;

-- 7c. Top 10 pin codes by transaction value
SELECT state, entity_name AS pincode,
       SUM(transaction_count) AS total_count,
       ROUND(SUM(transaction_amount)/1000000, 2) AS total_millions
FROM top_transaction
WHERE entity_type = 'pincodes'
GROUP BY state, entity_name
ORDER BY total_millions DESC
LIMIT 10;

-- 7d. Year-quarter wise top performing state
SELECT year, quarter, state,
       SUM(transaction_amount) AS total_amount
FROM top_transaction
GROUP BY year, quarter, state
ORDER BY year, quarter, total_amount DESC;