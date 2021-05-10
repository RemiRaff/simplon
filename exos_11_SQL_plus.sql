-- 11._Interroger_une_base_de_donnees_pour_aller_plus_loin
-- https://sql.sh/fonctions/agregation/sum
-- https://www.w3resource.com/mysql/mysql-functions-and-operators.php

USE sakila;


-- 1- Afficher les 10 locations les plus longues (nom/prenom client, film, video club, durée)
SELECT DISTINCT first_name AS Prénom,
       last_name AS Nom,
       title AS titre,
       store.store_id,
       TIMESTAMPDIFF(HOUR,return_date,rental_date) AS Durée_timestampdiff,
       datediff(return_date,rental_date) AS Durée_datediff -- ,return_date,rental_date présence de doublons...
FROM customer
JOIN store ON store.store_id=customer.store_id
JOIN inventory ON inventory.store_id=store.store_id
JOIN film ON film.film_id=inventory.film_id
JOIN rental ON rental.customer_id=customer.customer_id
ORDER BY Durée_datediff DESC
LIMIT 10;


-- 2- Afficher les 10 meilleurs clients actifs par montant dépensé (nom/prénom client, montant dépensé)
SELECT first_name AS Prénom,
       last_name AS Nom,
       SUM(amount) AS Montant, customer.customer_id
FROM customer
JOIN payment ON payment.customer_id=customer.customer_id
GROUP BY customer.customer_id -- customer_id doit être dans SELECT ???
ORDER BY Montant DESC
LIMIT 10;


-- 3- Afficher la durée moyenne de location par film triée de manière descendante
SELECT title, AVG(datediff(return_date,rental_date)) AS Durée -- , film.film_id on peut utiliser timestampdiff
FROM film
JOIN inventory ON inventory.film_id=film.film_id
JOIN rental ON rental.inventory_id=inventory.inventory_id
GROUP BY film.film_id
ORDER BY Durée DESC;


-- 4- Afficher tous les films n'ayant jamais été empruntés
SELECT film.film_id, title, COUNT(rental_date) AS Nb_emprunt
FROM film
JOIN inventory ON inventory.film_id=film.film_id
JOIN rental ON rental.inventory_id=inventory.inventory_id
GROUP BY film.film_id
HAVING Nb_emprunt=0; -- pas de résultat

SELECT film.film_id, title
FROM film
WHERE rental_duration=0; -- pas de résultat

SELECT title
FROM film
WHERE title NOT IN(SELECT title
                   FROM film
                   JOIN inventory ON inventory.film_id=film.film_id
                   JOIN rental ON rental.inventory_id=inventory.inventory_id
                   WHERE NOT ISNULL(rental_date));
-- R 42 rows


-- 5- Afficher le nombre d'employés (staff) par video club
SELECT store.store_id, COUNT(staff_id) as Nb_Employés
FROM store
JOIN staff ON staff.store_id=store.store_id
GROUP BY store_id;


-- 6- Afficher les 10 villes avec le plus de video clubs
SELECT city, COUNT(store_id) AS nb_clubs
FROM city
JOIN address ON address.city_id=city.city_id
JOIN store ON store.address_id=address.address_id
GROUP BY city
ORDER BY nb_clubs DESC
LIMIT 10;


-- 7- Afficher le film le plus long dans lequel joue Johnny Lollobrigida
SELECT title, film.length, first_name, last_name
FROM film
JOIN film_actor ON film_actor.film_id=film.film_id
JOIN actor ON actor.actor_id=film_actor.actor_id
WHERE first_name="JOHNNY"
      AND
      last_name="LOLLOBRIGIDA"
ORDER BY film.length DESC
LIMIT 1;


-- 8- Afficher le temps moyen de location du film 'Academy dinosaur'
SELECT title, rental_duration
FROM film
WHERE title="ACADEMY DINOSAUR"; -- R: 'ACADEMY DINOSAUR', '6'

SELECT title, AVG(datediff(return_date,rental_date)) AS Temps_moy_loc
from film
JOIN inventory ON inventory.film_id=film.film_id
JOIN rental ON rental.inventory_id=inventory.inventory_id
WHERE title="ACADEMY DINOSAUR"
GROUP BY film.title;


-- 9- Afficher les films avec plus de deux exemplaires en inventaire (store id, titre du film, nombre d'exemplaires)
SELECT store.store_id, film.title, film.film_id , COUNT(film.film_id) AS Nb_exemplaires
FROM film
JOIN inventory ON inventory.film_id=film.film_id
JOIN store ON inventory.store_id=store.store_id
GROUP BY store.store_id, film.title, film.film_id -- Pourquoi obliger de tout mettre??? 
HAVING Nb_exemplaires>2;


-- 10- Lister les films contenant 'din' dans le titre
SELECT film.title -- , SUBSTR(film.title,1,1) -- index ne commence pas à 0 mais à 1
FROM film
-- WHERE SUBSTRING(film.title,1,3)='DIN' -- commence avec DIN
WHERE POSITION('DIN' in film.title)>0;


-- 11- Lister les 5 films les plus empruntés
SELECT title, COUNT(title) AS Nb_emprunts -- , rental.rental_id
FROM film
JOIN inventory ON inventory.film_id=film.film_id
JOIN rental ON rental.inventory_id=inventory.inventory_id
GROUP BY title
ORDER BY Nb_emprunts DESC
LIMIT 5;


-- 12- Lister les films sortis en 2003, 2005 et 2006
SELECT title, release_year
FROM film
WHERE release_year=2003 -- 0 résultat
	  OR
      release_year=2005 -- 0 résultat
      OR
      release_year=2006; -- tous sortis en 2006


-- 13- Afficher les films ayant été empruntés mais n'ayant pas encore été restitués, triés par date d'emprunt. Afficher seulement les 10 premiers.
SELECT title -- , rental_date , return_date
FROM film
JOIN inventory ON inventory.film_id=film.film_id
JOIN rental ON rental.inventory_id=inventory.inventory_id
-- WHERE return_date = NULL -- ne marche pas
WHERE ISNULL(return_date)
ORDER BY rental_date
LIMIT 10;


-- 14- Afficher les films d'action durant plus de 2h
SELECT title, category.name, film.length AS Durée
FROM film
JOIN film_category ON film_category.film_id = film.film_id
JOIN category ON category.category_id = film_category.category_id
WHERE category.name = 'ACTION'
      AND
      film.length > 120; -- durée en minutes, Durée ne fonctionne pas


-- 15- Afficher tous les utilisateurs ayant emprunté des films avec la mention NC-17
SELECT customer.first_name, customer.last_name, film.title, film.rating
FROM customer
JOIN rental ON rental.customer_id=customer.customer_id
JOIN inventory ON inventory.inventory_id=rental.inventory_id
JOIN film ON film.film_id = inventory.film_id
WHERE film.rating = 'NC-17';


-- 16- Afficher les films d'animation dont la langue originale est l'anglais
SELECT title, category.name, language.name
FROM film
JOIN film_category ON film_category.film_id = film.film_id
JOIN category ON category.category_id = film_category.category_id
JOIN language ON language.language_id = film.language_id
WHERE category.name = 'ANIMATION'
	  AND
      language.name = 'English'; -- tous en English


-- 17- Afficher les films dans lesquels une actrice nommée Jennifer a joué (bonus: en même temps qu'un acteur nommé Johnny)
SELECT title, actor.first_name
FROM film
JOIN film_actor ON film_actor.film_id=film.film_id
JOIN actor ON actor.actor_id=film_actor.actor_id
WHERE actor.first_name="JENNIFER" -- 22 films
      -- AND actor.first_name="JOHNNY" fonctionne pas car même champ
      AND
      title IN(SELECT title
               FROM film
               JOIN film_actor ON film_actor.film_id=film.film_id
               JOIN actor ON actor.actor_id=film_actor.actor_id
               WHERE actor.first_name="JOHNNY"); -- juste 'INSTINCT AIRPORT', 'JENNIFER'


-- 18- Quelles sont les 3 catégories les plus empruntées?
SELECT category.name, COUNT(category.name) AS Nb_emprunts
FROM category
JOIN film_category ON film_category.category_id = category.category_id
JOIN film ON film.film_id = film_category.film_id
JOIN inventory ON inventory.film_id = film.film_id
JOIN rental ON rental.inventory_id = inventory.inventory_id
WHERE NOT ISNULL(rental_date)
GROUP BY category.name
ORDER BY Nb_emprunts DESC
LIMIT 3;


-- 19- Quelles sont les 10 villes où on a fait le plus de locations?
SELECT city.city, COUNT(rental_date) AS Nb_locs
FROM city
JOIN address ON address.city_id = city.city_id
JOIN customer ON customer.address_id = address.address_id
JOIN rental ON rental.customer_id = customer.address_id
GROUP BY city.city
ORDER BY Nb_locs DESC
LIMIT 10;
-- ERROR Enable to inilize Spatial Viewer => libproj avec SELECT *


-- 20- Lister les acteurs ayant joué dans au moins 1 film
SELECT actor.first_name, actor.last_name, COUNT(actor.last_name) AS Nb_films
FROM actor
JOIN film_actor ON film_actor.actor_id = actor.actor_id
JOIN film ON film_actor.film_id = film.film_id
-- WHERE Nb_films = 0 ERREUR: faut utiliser HAVING
GROUP BY actor.last_name, actor.first_name
HAVING Nb_films>=1; -- =0 pas de résultat, tous les acteurs ont joué dans au moins 1 film
