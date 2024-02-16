# **
# Shebang
# Title, author
# Docstrings

import sqlite3
# import the sqlite3 library

#~ import pdb
#~ pdb.set_trace()
# Also type commands in sqlite3, to figure out what script does

conn = sqlite3.connect('../Data/test.db')
# create a connection to the database

c = conn.cursor()
# to execute commands, create a "cursor"

c.execute('''CREATE TABLE Test
	(ID INTEGER PRIMARY KEY,
	MyVal1 INTEGER,
	MyVal2 TEXT)''')
# use the cursor to execute the queries
# use the triple single quote to write queries on several lines

#~ c.execute('''DROP TABLE test''')

c.execute('''INSERT INTO Test VALUES
	(NULL, 3, 'mickey')''')

c.execute('''INSERT INTO Test VALUES
	(NULL, 4, 'mouse')''')
# insert the records. note that because
# we set the primary key, it will auto-increment
# therefore, set it to NULL

conn.commit()
# when you "commit", all the commands will
# be executed

c.execute("SELECT * FROM TEST")
# now we select the records

# access the next record:
print c.fetchone()
print c.fetchone()

# let's get all the records at once
c.execute("SELECT * FROM TEST")
print c.fetchall()

manyrecs = [(5, 'goofy'),
	(6, 'donald'),
	(7, 'duck')]
# insert many records at once:
# create a list of tuples

c.executemany('''INSERT INTO test
	VALUES(NULL, ?, ?)''', manyrecs)
# now call executemany

conn.commit()
# and commit

for row in c.execute('SELECT * FROM test'):
	print 'Val', row[1], 'Name', row[2]
# now let's fetch the records
# we can use the query as an iterator!

# close the connection before exiting
conn.close()


# DELETE
########################################
# Make a database in memory, without using the disk
########################################

import sqlite3

conn = sqlite3.connect(":memory:")

c = conn.cursor()

c.execute("CREATE TABLE tt (Val TEXT)")

conn.commit()

z = [('a',), ('ab',), ('abc',), ('b',), ('c',)]

c.executemany("INSERT INTO tt VALUES (?)", z)

conn.commit()

c.execute("SELECT * FROM tt WHERE Val LIKE 'a%'").fetchall()

conn.close()
