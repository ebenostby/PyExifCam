#   Copyright 2022 Eben Ostby
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License. 

import sqlite3
import re
class Db:
	def __init__(self, name):
		self.name = name
		self.nonblanks = re.compile(r'\S')

		conn = sqlite3.connect(self.name)

		# Create a cursor instance
		c = conn.cursor()

		# Create Table
		c.execute("""CREATE TABLE IF NOT EXISTS cameras (
					id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
					maker TEXT NOT NULL,
					model TEXT
					)""")
		c.execute("""CREATE TABLE IF NOT EXISTS lenses (
					id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
					cameraid INT,
					maker TEXT NOT NULL,
					model TEXT,
					length INT,
					aperture FLOAT
				)""")
		c.execute("""CREATE TABLE IF NOT EXISTS state (
					name TEXT NOT NULL,
					value TEXT
		)""")
		# Commit changes
		conn.commit()
		conn.close()
	
	def getstate(self, statename):
		conn = sqlite3.connect(self.name)

		# Create a cursor instance
		c = conn.cursor()

		c.execute("SELECT value FROM state WHERE name = ?", (statename,))
		values = c.fetchall()	
		conn.commit()
		conn.close()
		return values
	def setstate(self, name, value):
		conn = sqlite3.connect(self.name)

		# Create a cursor instance
		c = conn.cursor()

		c.execute("DELETE FROM state WHERE name = ?", (name,))
		c.execute("INSERT INTO state (name, value) VALUES (?, ?)", (name, value))	
		conn.commit()
		conn.close()
	

	def query(self):
		# Clear the Treeview
		# do this before the call
		#for record in my_tree.get_children():
		#	my_tree.delete(record)
		
		# Create a database or connect to one that exists
		conn = sqlite3.connect(self.name)

		# Create a cursor instance
		c = conn.cursor()

		c.execute("SELECT cameras.id, cameras.maker, cameras.model FROM cameras ORDER BY cameras.id")
		cams = c.fetchall()
		c.execute("SELECT lenses.id, lenses.cameraid, lenses.maker, lenses.model, lenses.length, lenses.aperture  FROM lenses ORDER BY lenses.id")
		lens = c.fetchall()
		#for record in records:
		#	print(record)
		# Commit changes
		conn.commit()

		# Close our connection
		conn.close()
		self.cams = cams
		self.lens = lens
	def updateCamera(self, id, maker, model):
		conn = sqlite3.connect(self.name)
		if ((maker == None) or self.nonblanks.search(str(maker)) == None):
			maker = "Unknown"
		if ((model == None) or self.nonblanks.search(str(model)) == None):
			model = "Unknown"
		c = conn.cursor()
		c.execute("""UPDATE cameras SET maker = ?, model=? WHERE id =? """, (str(maker), str(model), id))
		conn.commit()
		conn.close()
	def deleteCamera(self, id):
		conn = sqlite3.connect(self.name)
		c = conn.cursor()
		c.execute("""DELETE FROM cameras  WHERE id =? """, (id,))
		c.execute("""DELETE FROM lenses WHERE cameraid=?""", (id,))
		conn.commit()
		conn.close()
	def deleteLens(self, id):
		conn = sqlite3.connect(self.name)
		c = conn.cursor()
		c.execute("""DELETE FROM lenses WHERE id=?""", (id,))
		conn.commit()
		conn.close()
	
	def newLens(self, cameraid, maker, model, length, aperture):
		conn = sqlite3.connect(self.name)
		c = conn.cursor()
		if ((maker == None) or self.nonblanks.search(maker) == None):
			maker = "Unknown"
		if ((model == None) or self.nonblanks.search(model) == None):
			model = "Unknown"
		c.execute("""INSERT INTO lenses (cameraid, maker, model,  length, aperture) VALUES (?, ?, ?, ?, ?)""", (cameraid, str(maker), str(model), length, aperture))
		lastrowid = c.lastrowid
		conn.commit()
		conn.close()
		return lastrowid
		
	def updateLens(self, id, maker, model, length, aperture):
		conn = sqlite3.connect(self.name)
		if ((maker == None) or self.nonblanks.search(maker) == None):
			maker = "Unknown"
		if ((model == None) or self.nonblanks.search(model) == None):
			model = "Unknown"
		c = conn.cursor()
		c.execute("""UPDATE lenses SET maker = ?, model = ?,  length = ?, aperture = ? where id = ?""", (str(maker), str(model), length, aperture, id))
		conn.commit()
		conn.close()
		
	def newCamera(self, maker, model):
		conn = sqlite3.connect(self.name)
		if ((maker == None) or self.nonblanks.search(maker) == None):
			maker = "Unknown"
		if ((model == None) or self.nonblanks.search(model) == None):
			model = "Unknown"
		c = conn.cursor()
		c.execute("""INSERT INTO cameras (maker, model) VALUES (?, ?)""", (str(maker), str(model)))
		lastrowid = c.lastrowid
		conn.commit()
		conn.close()
		return lastrowid

	def getCams(self):
		return self.cams
	def getLens(self):
		return self.lens
		
