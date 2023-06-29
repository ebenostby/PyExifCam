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


import tkinter
from .db import Db
import os
from .olddb import OldDb
from .interactive import Interactive
from .menus import BuildMenus
from pathlib import Path
from tkinter.messagebox import showerror

appsup = "~/Library/Application Support/ExifCam"
dbname = "cam.db"

def main():
	root = tkinter.Tk()
	root.title('camera exif tool')
	root.geometry("1000x600")
	

	myappsup = Path(appsup).expanduser()
	myappsup.mkdir(parents=True,exist_ok=True)
	database = str(myappsup / dbname)
	
	
	db = Db(database)
	inter = Interactive(root, db)
	BuildMenus(root, inter, True)
	root.tk.createcommand("::tk::mac::OpenDocument", lambda *x:inter.fileRequest(x))
# Run to pull data from database on start
	db.query()
	cams = db.getCams()
	lens = db.getLens()
	# optionally transition from AnalogExif
	if (len(cams) == 0):
		analogexifdir=os.path.expanduser("~/Library/Application Support/AnalogExif")
		olddb = OldDb(analogexifdir, "Untitled.ael")
		if (olddb.query()):
			olddb.populate(db)
			db.query()
			cams = db.getCams()
			lens = db.getLens()
	
	inter.insert(cams, lens)
	inter.setInitialFocus(db.getstate("selected"))
	root.mainloop()