USE sakila;

-- https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html
-- http://perso.univ-lemans.fr/~cpiau/BD/SQL_PAGES/SQL2.htm

-- 11._Interroger_une_base_de_donnees

-- ================= Interrogations avancées
SET lc_time_names = 'fr_fr'; -- affiche le mois février plutôt que febuary

-- requête 1: afficher le mois des emprunts 2006
SELECT monthname(rental_date)
FROM rental
WHERE year(rental_date)="2006";

-- requête 2: afficher durée de loc en jour
SELECT datediff(return_date,rental_date) AS Durée-- ,return_date,rental_date
FROM rental;

-- requête 3: afficher emprunt 2005 avant 1h du matin
SELECT date_format(rental_date,'%W %d %M %Y') -- ,rental_date
FROM rental
WHERE year(rental_date)=2005 and hour(rental_date)<1;

-- requête 4: afficher les emprunts entre avril et mai, triés du plus vieux au + récent
SELECT rental_date
FROM rental
WHERE 4<=month(rental_date) and month(rental_date)<=5
ORDER BY rental_date;

-- requête 5: Lister les films dont le nom ne commence pas par le « Le »
SELECT title
FROM film
WHERE instr(title,'LE')!=1;
-- ORDER BY title a=>z

-- requête 6: Lister les films ayant la mention « PG-13 » ou « NC-17 ».
--            Ajouter une colonne qui affichera « oui » si « NC-17 » et « non » Sinon.
SELECT title,rating, CASE rating
					   WHEN "NC-17" then "Oui"
                       ELSE "Non"
                       END AS "NC-17"
FROM film
WHERE rating="PG-13" OR rating="NC-17";

-- requête 7: Fournir la liste des catégories qui commencent par un ‘A’ ou un ‘C’. (Utiliser LEFT).
SELECT DISTINCT name
FROM category
WHERE LEFT(name,1)='A' or LEFT(name,1)='C';

-- requête 8: Lister les trois premiers caractères des noms des catégories.
SELECT DISTINCT LEFT(name,3)
FROM category;

-- requête 9: Lister les premiers acteurs en remplaçant dans leur prenom les E par des A.
SELECT first_name, replace(first_name,'E','A') AS REQ_9 , last_name
FROM actor;

-- ================= JOINTURES
-- 1. Lister les 10 premiers films ainsi que leur langue.
SELECT title,language.name
FROM film
JOIN language ON film.language_id = language.language_id
LIMIT 10;

-- 2. Afficher les films dans lesquels a joué « JENNIFER DAVIS » et sortie en 2006.
SELECT title -- ,actor.last_name,film.release_year
FROM film
JOIN film_actor on film.film_id=film_actor.film_id
JOIN actor on actor.actor_id=film_actor.actor_id
WHERE actor.first_name="JENNIFER"
      AND
      actor.last_name="DAVIS"
      AND
      film.release_year=2006;

-- 3. Afficher le nom des clients ayant empruntés « ALABAMA DEVIL ».
SELECT first_name AS Prénom,last_name AS NOM -- ,film.title
FROM customer
JOIN rental on rental.customer_id=customer.customer_id
JOIN inventory on inventory.inventory_id=rental.inventory_id
JOIN film on film.film_id=inventory.film_id
WHERE film.title="ALABAMA DEVIL";

-- 4. Afficher les films louer par des personne habitant à « Woodridge ».
--    Vérifié s’il y a des films qui n’ont jamais été emprunté.
SELECT film.title, city.city
FROM film
JOIN inventory ON film.film_id=inventory.film_id
JOIN store ON inventory.store_id=store.store_id
JOIN customer ON store.store_id=customer.store_id
JOIN address ON address.address_id=customer.address_id
JOIN city ON address.city_id=city.city_id
WHERE city.city="Woodridge"; -- pas de résultat

-- SELECT * FROM city WHERE city="Woodridge"
-- SELECT DISTINCT * FROM city

SELECT film.title -- ,rental.rental_date,rental.return_date
FROM film
JOIN inventory ON inventory.film_id=film.film_id
JOIN rental ON rental.inventory_id=inventory.inventory_id
WHERE ISNULL(rental_date); -- pas de résultat
-- WHERE ISNULL(return_date) -- return_date = NULL ne donne rien

-- 5. Quel sont les 10 films dont la durée d’emprunt à été la plus courte ?
SELECT DISTINCT film.title,datediff(return_date,rental_date) AS Durée ,return_date -- pour ODER il faut l'afficher
FROM film
JOIN inventory ON inventory.film_id=film.film_id
JOIN rental ON rental.inventory_id=inventory.inventory_id
WHERE NOT ISNULL(return_date) -- fonctionne pas avec Durée
ORDER BY Durée
LIMIT 10;

-- 6. Lister les films de la catégorie « Action » ordonnés par ordre alphabétique.
SELECT film.title -- ,category.name
FROM film
JOIN film_category ON film_category.film_id = film.film_id
JOIN category ON category.category_id=film_category.category_id
WHERE category.name="Action"
ORDER BY film.title;

-- 7. Quels sont les films dont la duré d’emprunt à été inférieur à 2 jour ?
SELECT DISTINCT film.title, datediff(return_date,rental_date) AS Durée, return_date
FROM film
JOIN inventory ON inventory.film_id=film.film_id
JOIN rental ON rental.inventory_id=inventory.inventory_id
WHERE datediff(return_date,rental_date)<2;