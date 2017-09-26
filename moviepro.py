import sqlite3 as lite
import csv
import pandas as pd
import sys
con = lite.connect('cs1656.sqlite')

with con:
	cur = con.cursor() 

	########################################################################		
	### CREATE TABLES ######################################################
	########################################################################		
	# DO NOT MODIFY - START 
	cur.execute('DROP TABLE IF EXISTS Actors')
	cur.execute("CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

	cur.execute('DROP TABLE IF EXISTS Movies')
	cur.execute("CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

	cur.execute('DROP TABLE IF EXISTS Directors')
	cur.execute("CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

	cur.execute('DROP TABLE IF EXISTS Cast')
	cur.execute("CREATE TABLE Cast(aid INT, mid INT, role TEXT)")

	cur.execute('DROP TABLE IF EXISTS Movie_Director')
	cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")
	# DO NOT MODIFY - END

	########################################################################		
	### READ DATA FROM FILES ###############################################
	########################################################################		
	# actors.csv, movies.csv, directors.csv, cast.csv, movie_director.csv
	# UPDATE THIS

	########################################################################		
	### INSERT DATA INTO DATABASE ##########################################
	########################################################################		
	# UPDATE THIS


	with open("all_actors.csv", "r") as f:
		reader = csv.reader(f, delimiter=",")	
		for record in reader:	
			#print(record)				
			cur.execute("INSERT INTO Actors VALUES(?, ?, ?, ?)", record) 

	with open("all_cast.csv", "r") as f:
		reader = csv.reader(f, delimiter=",")	
		for record in reader:				
			#print(record)				
			cur.execute("INSERT INTO Cast VALUES(?, ?, ?)", record) 

	with open("all_directors.csv", "r") as f:
		reader = csv.reader(f, delimiter=",")	
		for record in reader:				
			#print(record)				
			cur.execute("INSERT INTO Directors VALUES(?, ?, ?)", record) 

	with open("all_movies.csv", "r") as f:
		reader = csv.reader(f, delimiter=",")	
		for record in reader:				
			#print(record)				
			cur.execute("INSERT INTO Movies VALUES(?, ?, ?, ?)", record) 

	with open("all_movie_dir.csv", "r") as f:
		reader = csv.reader(f, delimiter=",")	
		for record in reader:	
			#print(record)				
			cur.execute("INSERT INTO Movie_Director VALUES(?, ?)", record) 

#	cur.execute("INSERT INTO Actors VALUES(1001, 'Harrison', 'Ford', 'Male')") 
#	cur.execute("INSERT INTO Actors VALUES(1002, 'Daisy', 'Ridley', 'Female')")   

#	cur.execute("INSERT INTO Movies VALUES(101, 'Star Wars VII: The Force Awakens', 2015, 8.2)") 
#	cur.execute("INSERT INTO Movies VALUES(102, 'Rogue One: A Star Wars Story', 2016, 8.0)")
	
#	cur.execute("INSERT INTO Cast VALUES(1001, 101, 'Han Solo')")  
#	cur.execute("INSERT INTO Cast VALUES(1002, 101, 'Rey')")  

#	cur.execute("INSERT INTO Directors VALUES(5000, 'J.J.', 'Abrams')")  
	
#	cur.execute("INSERT INTO Movie_Director VALUES(5000, 101)")  

	con.commit()	

	########################################################################		
	### QUERY SECTION ######################################################
	########################################################################		
	queries = {}

	# DO NOT MODIFY - START 	
	# DEBUG: all_movies ########################
	queries['all_movies'] = '''
SELECT * FROM Movies
'''	
	# DEBUG: all_actors ########################
	queries['all_actors'] = '''
SELECT * FROM Actors
'''	
	# DEBUG: all_cast ########################
	queries['all_cast'] = '''
SELECT * FROM Cast
'''	
	# DEBUG: all_directors ########################
	queries['all_directors'] = '''
SELECT * FROM Directors
'''	
	# DEBUG: all_movie_dir ########################
	queries['all_movie_dir'] = '''
SELECT * FROM Movie_Director
'''	
	# DO NOT MODIFY - END

	########################################################################		
	### INSERT YOUR QUERIES HERE ###########################################
	########################################################################		
#Actors (aid, fname, lname, gender)
#Movies (mid, title, year, rank)
#Directors (did, fname, lname)
#Cast (aid, mid, role)
#Movie_Director (did, mid)
	# Q1 ########################	
	# List all the actors (first and last name) who acted in 
	#at least one film in the 1st half of the 20th century (1901-1950) 
	#and in at least one film in the 2nd half of the 20th century (1951 - 2000).	
	queries['Q1'] = '''
 SELECT fname, lname FROM Actors WHERE EXISTS(
 	SELECT * FROM Movies as M JOIN Cast as C ON C.mid = M.mid
 	WHERE Actors.aid = C.aid AND M.year > 1900 AND M.year < 1951)
	AND EXISTS(	SELECT * FROM Movies as M JOIN Cast as C ON C.mid = M.mid
 	WHERE Actors.aid = C.aid AND M.year > 1950 AND M.year <= 2000)
'''	
	
	# Q2 ########################		
	# List all the movies (title, year) that were released in the same
	# year as the movie entitled "Rogue One: A Star Wars Story", but had
	# a better rank (Note: the higher the value in the rank attribute, 
	#the better the rank of the movie).
	queries['Q2'] = '''
SELECT M.title, M.year FROM Movies as M WHERE 
	M.year = (SELECT F.year From Movies as F WHERE F.title = 'Rogue One: A Star Wars Story')
	AND M.rank > (SELECT F.rank From Movies as F WHERE F.title = 'Rogue One: A Star Wars Story')
'''	
#Actors (aid, fname, lname, gender)
#Movies (mid, title, year, rank)
#Directors (did, fname, lname)
#Cast (aid, mid, role)
#Movie_Director (did, mid)
	# Q3 ########################		
	#List all the actors (first and last name) who played
	# in the movie entitled "Star Wars VII: The Force Awakens".
	queries['Q3'] = '''
SELECT fname, lname FROM Actors WHERE aid = (
	SELECT c.aid FROM Movies as M JOIN Cast as C ON C.mid = M.mid 
	WHERE M.title = 'Star Wars VII: The Force Awakens'
	and c.aid = Actors.aid) 
'''	

	# Q4 ########################	
	#Find the actor(s) (first and last name) who 
	#only acted in films released before 1985.		
	queries['Q4'] = '''
SELECT fname, lname FROM Actors WHERE NOT EXISTS(
	SELECT * FROM Movies as M JOIN Cast as C ON C.mid = M.mid
 	WHERE Actors.aid = C.aid AND M.year > 1985)
	
'''	
#Actors (aid, fname, lname, gender)
#Movies (mid, title, year, rank)
#Directors (did, fname, lname)
#Cast (aid, mid, role)
#Movie_Director (did, mid)
	# Q5 ########################	
	#List all the directors in descending order of
	#the number of films they directed (first name, last name, number
	#of films directed).
	queries['Q5'] = '''
SELECT fname, lname, COUNT(*) FROM Directors D Join Movie_Director M on D.did = M.did
GROUP BY fname, lname
ORDER BY COUNT(*) DESC
'''		

	# Q6 ########################
	#Find the movie(s) with the largest cast 
	#(title, number of cast members). Note: show all movies in 
	#case of a tie.		
	queries['Q6'] = '''
WITH y AS (SELECT title, COUNT(*) as num FROM Cast C JOIN Movies M on C.mid = M.mid
GROUP BY title)
SELECT title, y.num FROM y
WHERE y.num = (SELECT MAX(x.num) FROM y as x)

'''	

	# Q7 ########################	
	#Find the movie(s) whose cast has more actresses than actors (i.e., gender=female vs gender=male). Show the title,
	#the number of actresses, and the number of actors in the results.	
	queries['Q7'] = '''
WITH female AS (SELECT mid, COUNT(*) as Fnum 
FROM Cast C JOIN Actors A on C.aid = A.aid
WHERE A.gender = 'Female'
GROUP By mid)

select K.title as title, D.Fnum as female_num, D.Mnum as male_num From Movies K JOIN (
select F.mid,
CASE WHEN Mnum is NULL THEN 0 ELSE Mnum end AS Mnum, 
CASE WHEN Fnum is NULL THEN 0 ELSE Fnum end AS Fnum 
From female F LEFT OUTER JOIN (SELECT mid, COUNT(*) as Mnum
FROM Cast C JOIN Actors A on C.aid = A.aid
WHERE A.gender = 'Male'
GROUP By mid) M on M.mid = F.mid) D on D.mid = K.mid
WHERE D.Fnum > D.Mnum

'''	
#Actors (aid, fname, lname, gender)
#Movies (mid, title, year, rank)
#Directors (did, fname, lname)
#Cast (aid, mid, role)
#Movie_Director (did, mid)
	# Q8 ########################		
	#Find all the actors who have worked with at least 7 different directors (i.e., acted
	#in at least 7 different movies with distinct directors). Show the actor's first, last 
	#name, and the number of directors he/she has worked with.
	queries['Q8'] = '''
SELECT fname, lname, c_d FROM (
SELECT aid, fname, lname, count(distinct did) as c_d FROM (SELECT * FROM (SELECT * 
FROM (SELECT * FROM Actors A JOIN Cast C on A.aid = C.aid) AC 
JOIN Movies M on M.mid = AC.mid) ACM JOIN movie_director MD on MD.mid = ACM.mid)
GROUP BY aid, fname, lname	
HAVING c_d >= 7)

'''	
#Actors (aid, fname, lname, gender)
#Movies (mid, title, year, rank)
#Directors (did, fname, lname)
#Cast (aid, mid, role)
#Movie_Director (did, mid)
	# Q9 ########################	
	#For every actor, count the movies that he/she appeared in his/her debut year
	# (i.e., year of their first movie). Show the actor's first and last name, plus the count. Sort by decreasing order of the count.
	queries['Q9'] = '''
WITH min_year as (SELECT MIN(year) as Min, M.mid, aid, fname, lname 
FROM (SELECT * FROM Actors A JOIN Cast C on A.aid = C.aid) AC 
JOIN Movies M on M.mid = AC.mid
GROUP By aid) 

SELECT fname, lname, COUNT(*)
FROM (SELECT * FROM Actors A JOIN Cast C on A.aid = C.aid) AC 
JOIN Movies M on M.mid = AC.mid
WHERE M.year = (
SELECT Min FROM min_year M WHERE M.aid = AC.aid)
GROUP BY fname, lname
ORDER BY COUNT(*) DESC
'''		

	# Q10 ########################
	#Find instances of nepotism between actors and directors, i.e., an actor in a movie and the director have the same last name. 
	#Show the last name and the title of the movie, sorted alphabetically by last name.
	queries['Q10'] = '''
SELECT ACMM.lname, ACMM.title FROM (SELECT * FROM (SELECT * FROM (SELECT * 
FROM Actors A JOIN Cast C on A.aid = C.aid) 
AC JOIN Movies M on AC.mid = M.mid) ACM JOIN Movie_Director MD on Md.mid = ACM.mid) ACMM 
JOIN Directors D on ACMM.did = D.did
WHERE ACMM.lname = D.lname
ORDER BY ACMM.lname, ACMM.title ASC
'''			
#Actors (aid, fname, lname, gender)
#Movies (mid, title, year, rank)
#Directors (did, fname, lname)
#Cast (aid, mid, role)
#Movie_Director (did, mid)
	# Q11 ########################	
	#The Bacon number of an actor is the length of the shortest path between the actor and Kevin Bacon in the "co-acting" graph. 
	#That is, Kevin Bacon has Bacon number 0; all actors who acted in the same movie as him have Bacon number 1; all actors who acted 
	#in the same film as some actor with Bacon number 1 have Bacon number 2, etc. List all actors whose Bacon number is 2
	# (first name, last name). You can familiarize yourself with the concept, by visiting The Oracle of Bacon.
	queries['Q11'] = '''
WITH Recursive bacon AS (SELECT C.aid, C.mid, 0 as rank
FROM Cast C JOIN Actors A on A.aid = C.aid WHERE A.fname = 'Kevin'
and A.lname = 'Bacon'
UNION ALL
SELECT C1.aid, C2.mid, B.rank + 1
FROM bacon B JOIN Cast C1 on C1.mid = B.mid
AND B.rank < 2
JOIN Cast C2 on C1.aid = C2.aid)

SELECT fname, lname FROM Actors WHERE aid IN 
(SELECT aid
FROM bacon 
GROUP BY aid
HAVING MIN(rank) = 2)  
'''		

	# Q12 ########################	
	# Assume that the popularity of an actor is reflected by the average rank of all the movies he/she has acted in. 
	#Find the top 20 most popular actors (in descreasing order of popularity) -- list the actor's first/last name, the total 
	#number of movies he/she has acted, and his/her popularity score. For simplicity, feel free to ignore ties at the number 20 spot 
	#(i.e., always show up to 20 only).
	queries['Q12'] = '''
SELECT fname, lname, COUNT(*), AVG(rank)
FROM (SELECT * FROM Actors A JOIN Cast C on A.aid = C.aid) AC 
JOIN Movies M on M.mid = AC.mid
GROUP BY aid, fname, lname
ORDER BY AVG(rank) DESC
LIMIT 20
'''		
#Actors (aid, fname, lname, gender)
#Movies (mid, title, year, rank)
#Directors (did, fname, lname)
#Cast (aid, mid, role)
#Movie_Director (did, mid)
	########################################################################		
	### SAVE RESULTS TO FILES ##############################################
	########################################################################		
	# DO NOT MODIFY - START 	
	for (qkey, qstring) in sorted(queries.items()):
		try:
			cur.execute(qstring)
			all_rows = cur.fetchall()
			
			print ("=========== ",qkey," QUERY ======================")
			print (qstring)
			print ("=========== ",qkey," RESULTS ====================")
			for row in all_rows:
				print (row)
			print (" ")

			with open(qkey+'.csv', 'w') as f:
				writer = csv.writer(f)
				writer.writerows(all_rows)
				f.close()
		
		except lite.Error as e:
			print ("An error occurred:", e.args[0])
	# DO NOT MODIFY - END
	
