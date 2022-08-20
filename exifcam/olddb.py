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

from tkinter import filedialog
import sqlite3
import re

class OldDb:
	def __init__(self, dir, name):

		ft = ( 
			("Image files", ".ael .sqlite"),
			("All files", ".*")
		)
		self.name=filedialog.askopenfilename(title="Import from Analog Exif?", initialdir=dir, initialfile=name,  filetypes=ft)

	def query(self):
		self.cams=False
		self.lens=False
		if (len(self.name) == 0):
			return False
		# Create a database or connect to one that exists
		conn = sqlite3.connect(self.name)

		# Create a cursor instance
		c = conn.cursor()

		c.execute("""SELECT A.GearId, A.TagValue, B.TagValue  
		FROM UserGearProperties A, UserGearProperties B, MetaTags AA, MetaTags BB 
		WHERE A.GearId = B.GearId 
		AND  A.TagId = AA.id AND AA.TagName = "Xmp.tiff.Make" 
		AND B.TagId = BB.id AND BB.TagName = "Xmp.tiff.Model"
""")
		cams=c.fetchall()

		c.execute("""SELECT P.ParentId, A.GearId,A.TagValue, B.TagValue, C.TagValue 
			FROM UserGearProperties A, UserGearProperties B, UserGearProperties C, MetaTags AA, MetaTags BB, MetaTags CC, UserGearItems P 
			WHERE P.id = A.GearId AND A.GearId = B.GearId AND B.GearId = C.GearId 
			AND  A.TagId = AA.id AND AA.TagName = "Xmp.aux.Lens,Xmp.MicrosoftPhoto.LensModel" 
			AND B.TagId = BB.id AND BB.TagName = "Xmp.MicrosoftPhoto.LensManufacturer" 
			AND C.TagId = CC.id AND CC.TagName = "Exif.Image.MaxApertureValue" 
			ORDER BY P.ParentId, A.GearId
""")
		lens = c.fetchall()
		# Commit changes
		conn.commit()

		# Close our connection
		conn.close()
		self.cams = cams
		self.lens = lens
		return True
	def populate(self, db):
		camLookup={}
		lookforlength=re.compile(r'\d+(?=\s*mm)')
		for i, cam in enumerate(self.cams):
			camLookup[cam[0]]=db.newCamera(cam[1], cam[2])
			print("Added", cam)
		for thislen in self.lens:
			length = 50.0
			if True:
				oldcamid = thislen[1] if (thislen[0]<0) else thislen[0]
				try:
					aperture = thislen[4].split('/',2)
					aperture = round(pow(2.0, int(aperture[0])/(2.0*int(aperture[1]))), 1)
				except:
					aperture = 3.5
				lengthstring = lookforlength.findall(thislen[2])
				if (len(lengthstring) > 0):
					length = int(lengthstring[0])
				db.newLens(camLookup[oldcamid], thislen[3], thislen[2], length,  aperture)
				# print("Added lens", thislen)
			else:
				print ("******* Cannot deal with lens", thislen)
		
	