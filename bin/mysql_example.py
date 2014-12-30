
import sqlite3 as sql
import os

#os.system('sqlite3 mediaManager.db')
con = lite.connect('/home/b40153/git/devel/torrents_manager/mediaManager.db')
cur = con.cursor()
#cur.execute("DROP TABLE IF EXISTS Series;")
#cur.execute("CREATE TABLE Series(Id INT, Serie TEXT, Season INT, Episode INT, EpisodeName TEXT, Synopsis TEXT, Aired DATE, Downloaded DATE, FileName TEXT, FileSize INT, FileLocation TEXT, videoResolution INT, Viewed DATE, Uploader TEXT, Subtitle TEXT)")
cur.execute("INSERT INTO Series VALUES(1,'Supernatural',5,12,'Something','Someone dies at the beggining and blood spills everywhere','2010-12-22','2010-12-25','supernaturalS05E12.mp4', 700, '/home/seriados/supernatural/season05', 720, '2010-12-26','eztv','ghostfacers')")
cur.execute("INSERT INTO Series VALUES(2,'Supernatural',5,11,'Something','Someone dies at the beggining and blood spills everywhere','2010-12-25','2010-12-26','supernaturalS05E11.mp4', 700, '/home/seriados/supernatural/season05', 720, '2010-12-27','eztv','ghostfacers')")
cur.execute("INSERT INTO Series VALUES(3,'Supernatural',5,14,'Something','Someone dies at the beggining and blood spills everywhere','2010-12-26','2010-12-27','supernaturalS05E14.mp4', 700, '/home/seriados/supernatural/season05', 720, '2010-12-28','eztv','ghostfacers')")
cur.execute("INSERT INTO Series VALUES(4,'Supernatural',5,15,'Something','Someone dies at the beggining and blood spills everywhere','2010-12-27','2010-12-28','supernaturalS05E15.mp4', 700, '/home/seriados/supernatural/season05', 720, '2010-12-29','eztv','ghostfacers')")
cur.execute('SELECT * FROM Series ORDER BY  Aired ASC')
rows = cur.fetchall()
for row in rows:
	print row
cur.execute("SELECT * FROM Series WHERE Serie LIKE 'Supernatural' ORDER BY  Aired DESC LIMIT 1");lastAired = cur.fetchall()[0]

#cur.execute("CREATE TABLE SeriesConfig(Name TEXT, IgnoreResolution TEXT, IgnoreUpReputation TEXT, folder TEXT, favTorUploader TEXT, favSubUploader TEXT)")
con.commit()
#cur.execute("CREATE TABLE torrentUploaders(Name TEXT, Ranking INT)")
#cur.execute("CREATE TABLE subtitleRanks(Name TEXT, Ranking INT)")
cur.execute("INSERT INTO SeriesConfig VALUES('Supernatural', 'True', 'False','/home/seriados/supernatural', 'eztv', 'noriegarj')")
cur.execute("INSERT INTO torrentUploaders VALUES('eztv',9)")
cur.execute("INSERT INTO torrentUploaders VALUES('rargb',8)")
cur.execute("INSERT INTO torrentUploaders VALUES('yifi',10)")
cur.execute("INSERT INTO subtitleRanks VALUES('Platinum',10)")
cur.execute("INSERT INTO subtitleRanks VALUES('Gold',9)")
cur.execute("INSERT INTO subtitleRanks VALUES('Silver',8)")
cur.execute("INSERT INTO SeriesConfig VALUES('Big Bang theory', 'True', 'True','/home/seriados/big-bang_theory', 'eztv', 'nerds')")
cur.execute('SELECT * FROM Series');rows = cur.fetchall();exec('for row in rows: \n  print row')
cur.execute('SELECT * FROM SeriesConfig');rows = cur.fetchall();exec('for row in rows: \n  print row')
cur.execute('SELECT * FROM torrentUploaders');rows = cur.fetchall();exec('for row in rows: \n  print row')
cur.execute('SELECT * FROM subtitleRanks');rows = cur.fetchall();exec('for row in rows: \n  print row')
cur.execute("SELECT name FROM sqlite_master")
for table in cur:
	print(table[0])

con.commit()
con.close()

