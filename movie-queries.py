import sqlite3 as lite
import csv
import pandas as pd
import sys
from neo4j.v1 import GraphDatabase, basic_auth


#driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "cs1656"), encrypted=False)
driver = GraphDatabase.driver("bolt://localhost", encrypted=False)
session = driver.session()

#Start new transaction
transaction = session.begin_transaction()

#[Q1] List all the actors who played in the movie entitled "Star Wars VII: The Force Awakens".
q1 = transaction.run("""
MATCH (m:Movie {title: 'Star Wars VII: The Force Awakens'})<-[:ACTS_IN]-(a:Actor)
RETURN a.name
;""")

print("Q1")
with open('output.txt', 'w', encoding="utf-8") as the_file:
	the_file.write('###Q1###\n')
	for record in q1:
		the_file.write(str(record) + '\n')
	the_file.write('\n')

#[Q2] List all the directors in descending order of the number of films they directed.
q2 = transaction.run("""
MATCH (d:Director)-[:DIRECTED]->(m:Movie)
WITH d, collect(m) AS movies
RETURN d.name, length(movies)
ORDER BY length(movies) DESC
;""")
#remove limit 

print("Q2")
with open('output.txt', 'a', encoding="utf-8") as the_file:
	the_file.write('###Q2###\n')
	for record in q2:
		the_file.write(str(record[0]) + ',' + str(record[1]) + '\n')
	the_file.write('\n')

#[q3] Find the movie with the largest cast.
#OUTPUT: movie_title, number_of_cast_members
q3 = transaction.run("""
MATCH (m:Movie)<-[:ACTS_IN]-(a:Actor)
WITH m, collect(a) AS cast
RETURN m.title, length(cast)
ORDER BY length(cast) DESC
limit 1
;""")

print("Q3")
with open('output.txt', 'a', encoding="utf-8") as the_file:
	the_file.write('###Q3###\n')
	for record in q3:
		the_file.write(str(record[0]) + ',' + str(record[1]) + '\n')
	the_file.write('\n')

#MATCH (d:Director)-[:DIRECTED]->(m:Movie),
#(a:Actor)-[:ACTS_IN]->(m:Movie)
#WITH a, m, collect(d) AS directed
#WHERE length(directed) >= 3
#RETURN a.name, length(directed)
#limit 4
#[q4] Find all the actors who have worked with at least 3 different directors (i.e., acted in at least 3 different movies with distinct directors).
#OUTPUT: actor_name, number_of_directors_he/she_has_worked_with
q4 = transaction.run("""
MATCH (d:Director)-[:DIRECTED]->(m:Movie)<-[:ACTS_IN]-(a:Actor)
WITH a, collect(d) as num
WHERE length(num) >= 3
RETURN a.name, length(num)
;""")
#remove limit 
print("Q4")
with open('output.txt', 'a', encoding="utf-8") as the_file:
	the_file.write('###Q4###\n')
	for record in q4:
		the_file.write(str(record[0]) + ',' + str(record[1]) + '\n')
	the_file.write('\n')

#[q5] The Bacon number of an actor is the length of the shortest path between the actor and Kevin Bacon in the "co-acting" graph. That is, Kevin Bacon has Bacon number 0; all actors who acted in the same movie as him have Bacon number 1; all actors who acted in the same film as some actor with Bacon number 1 have Bacon number 2, etc. List all actors whose Bacon number is 2 (first name, last name). You can familiarize yourself with the concept, by visiting The 
#OUTPUT: actor_name
q5 = transaction.run("""
MATCH (bacon:Actor{name: "Kevin Bacon"})-[:ACTS_IN]->(m:Movie)<-[:ACTS_IN]-(temp1:Actor)
MATCH (temp1:Actor)-[:ACTS_IN]->(n:Movie)<-[:ACTS_IN]-(temp2:Actor)
WHERE temp1 <> temp2 AND NOT (bacon)-[:ACTS_IN]->()<-[:ACTS_IN]-(temp2)
RETURN temp2.name
;""")
#remove limit 
print("q5")
with open('output.txt', 'a', encoding="utf-8") as the_file:
	the_file.write('###Q5###\n')
	for record in q5:
		the_file.write(str(record[0]) + '\n')
	the_file.write('\n')

#[q6] Extend the previous query to show all actors with a Bacon number of 1 to 4.
#OUTPUT: actor_name
q6 = transaction.run("""
MATCH (bacon:Person {name:"Kevin Bacon"})-[*1..4]-(temp:Actor)
RETURN DISTINCT temp.name
;""")
#remove limit 
print("q6")
with open('output.txt', 'a', encoding="utf-8") as the_file:
	the_file.write('###Q6###\n')
	for record in q6:
		the_file.write(str(record[0]) + '\n')
	the_file.write('\n')

#[q7] Find those actors who are not connected to Kevin Bacon in the co-acting graph (i.e., their Bacon number would be infinity).
#OUTPUT: actor_name
q7 = transaction.run("""
MATCH (n:Person)-[*]-(m:Actor)
with n as bacon, m as temp
WHERE NOT EXISTS((bacon{name:"Kevin Bacon"})-[*]-(temp))
RETURN DISTINCT temp.name
;""")

print("q7")
with open('output.txt', 'a', encoding="utf-8") as the_file:
	the_file.write('###Q7###\n')
	for record in q7:
		the_file.write(str(record[0]) + '\n')
	the_file.write('\n')

#[q8] Should the Kevin Bacon game be renamed? Is there a different actor with a higher number of first-level connections in the co-acting graph? Compute the number of co-actors for each actor and return the top 50 highest (sorted in descending order).
#OUTPUT: actor_name, number_of_co_actors
q8 = transaction.run("""
MATCH (p:Actor)-[:ACTS_IN]->(m:Movie)<-[:ACTS_IN]-(temp:Actor)
with p, count(temp) as num
RETURN p.name, num
ORDER BY num DESC
limit 50
;""")

print("q8")
with open('output.txt', 'a', encoding="utf-8") as the_file:
	the_file.write('###Q8###\n')
	for record in q8:
		the_file.write(str(record[0]) + ',' + str(record[1]) + '\n')
	the_file.write('\n')



transaction.close()
session.close()
