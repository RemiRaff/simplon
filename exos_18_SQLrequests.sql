-- 18._Requetes_agregation
USE sakila;


-- 1. Afficher le nombre de films dans les quels a joué l'acteur « JOHNNY LOLLOBRIGIDA », regroupé par catégorie.
SELECT category.name, COUNT(category.name) AS Nb_films
FROM film
JOIN film_actor ON film_actor.film_id = film.film_id
JOIN actor ON actor.actor_id = film_actor.actor_id
JOIN film_category ON film_category.film_id = film.film_id
JOIN category ON category.category_id = film_category.category_id
WHERE actor.first_name = "JOHNNY"
	  AND
      actor.last_name = "LOLLOBRIGIDA"
GROUP BY category.name;


-- 2. Ecrire la requête qui affiche les catégories dans les quels « JOHNNY LOLLOBRIGIDA » totalise plus de 3 films.
SELECT category.name, COUNT(category.name) AS Nb_films
FROM film
JOIN film_actor ON film_actor.film_id = film.film_id
JOIN actor ON actor.actor_id = film_actor.actor_id
JOIN film_category ON film_category.film_id = film.film_id
JOIN category ON category.category_id = film_category.category_id
WHERE actor.first_name = "JOHNNY"
	  AND
      actor.last_name = "LOLLOBRIGIDA"
GROUP BY category.name
HAVING Nb_films >= 3;


-- 3. Afficher la durée moyenne d'emprunt des films par acteurs.
SELECT actor.last_name, AVG(datediff(return_date,rental_date)) AS Duree_moy_emprunt
FROM actor
JOIN film_actor ON film_actor.actor_id = actor.actor_id
JOIN film ON film.film_id = film_actor.film_id
JOIN inventory ON inventory.film_id = film.film_id
JOIN rental ON rental.inventory_id = inventory.inventory_id
GROUP BY actor.last_name;


-- 4. L'argent total dépensé au vidéos club par chaque clients, classé par ordre décroissant.
SELECT customer.last_name, SUM(amount) AS Total
FROM customer
JOIN payment ON payment.customer_id = customer.customer_id
GROUP BY customer.customer_id
ORDER BY Total DESC;