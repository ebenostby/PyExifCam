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
	root.geometry("1000x550")
	

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