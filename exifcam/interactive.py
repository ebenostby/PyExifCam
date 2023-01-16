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
import os, re
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter.messagebox import showerror
from tkinter import filedialog
import subprocess

# from this and related tutorials https://tkinter.com/add-new-database-record-with-treeview-python-tkinter-gui-tutorial-177/
def treeview_sort_column(tv, col, reverse):
	print(col)
	if (col == "Maker"):
		l = [(tv.set(k, col)+"."+tv.set(k,'Camera'), k) for k in tv.get_children('')]
	else:
		l = [(tv.set(k, col), k) for k in tv.get_children('')]
	l.sort(reverse=reverse)

	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)

	# reverse sort next time
	tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

class Interactive:
	def __init__(self, root, db):
		self.db = db
		self.root = root
		self.desiredFiles = None
		self.justStarted = True
		mypath = os.path.abspath(os.path.dirname(__file__))
		if (os.path.exists(mypath+"/exiftool")):
			self.exiftool = mypath+"/exiftool"
		else:
			mypath = os.path.abspath(os.path.dirname(mypath))
			if (os.path.exists(mypath+"/exiftool")):
				self.exiftool = mypath+"/exiftool"
			else:
				raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "exiftool")

		self.tree_frame = tkinter.Frame(self.root)
		self.tree_frame.pack(pady=10)

		# Create a Treeview Scrollbar
		self.tree_scroll = tkinter.Scrollbar(self.tree_frame)
		self.tree_scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

		# Create The Treeview
		self.my_tree = tkinter.ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended", height=20)
		self.my_tree.pack()
		# a checkbox for an option
		self.minorErrors = tkinter.IntVar(value=0)
		c1 = ttk.Checkbutton(self.root, text='Fix errors & save backup',variable=self.minorErrors, onvalue=1, offvalue=0)
		c1.pack()
		self.textbox = tkinter.Label(self.root, text="")
		self.textbox.pack()
		# Configure the Scrollbar
		self.tree_scroll.config(command=self.my_tree.yview)

		# Define Our Columns
		self.my_tree['columns'] = ("ID", "Maker", "Camera", "Lens Maker", "Lens", "FL", "f/stop")

		# Format Our Columns
		self.my_tree.column("#0", width=20, stretch=tkinter.NO, anchor=tkinter.W)
		self.my_tree.column("ID", anchor=tkinter.W, width=30)
		self.my_tree.column("Maker", anchor=tkinter.W, width=140)
		self.my_tree.column("Camera", anchor=tkinter.W, width=140)
		self.my_tree.column("Lens Maker", anchor=tkinter.W, width=120)
		self.my_tree.column("Lens", anchor=tkinter.W, width=140)
		self.my_tree.column("FL", anchor=tkinter.CENTER, width=80)
		self.my_tree.column("f/stop", anchor=tkinter.CENTER, width=80)
		self.my_tree.heading("ID", text="ID", anchor=tkinter.W, command=lambda: treeview_sort_column(self.my_tree, "ID", False))
		self.my_tree.heading("Maker", text="Maker", anchor=tkinter.W, command=lambda: treeview_sort_column(self.my_tree, "Maker", False))
		self.my_tree.heading("Camera", text="Camera", anchor=tkinter.W, command=lambda: treeview_sort_column(self.my_tree, "Camera", False))
		self.my_tree.heading("Lens Maker", text="Lens Maker", anchor=tkinter.W, command=lambda: treeview_sort_column(self.my_tree, "Lens Maker", False))
		self.my_tree.heading("Lens", text="Model", anchor=tkinter.W, command=lambda: treeview_sort_column(self.my_tree, "Lens", False))
		self.my_tree.heading("FL", text="Length", anchor=tkinter.CENTER, command=lambda: treeview_sort_column(self.my_tree, "FL", False))
		self.my_tree.heading("f/stop", text="f/stop", anchor=tkinter.CENTER, command=lambda: treeview_sort_column(self.my_tree, "f/stop", False))
		

# Add tkinter.Buttons
#		button_frame = tkinter.LabelFrame(self.root, text="Commands")
#		button_frame.pack(fill="x", expand="yes", padx=20)

#		add_button = tkinter.Button(button_frame, text="+", command=self.addRow)
#		add_button.grid(row=0, column=1, padx=10, pady=10)

#		remove_one_button = tkinter.Button(button_frame, text="-", command=False)
#		remove_one_button.grid(row=0, column=2, padx=10, pady=10)


		# Bind the treeview
		self.my_tree.bind('<Double-Button-1>', self.onDoubleClick)
		self.my_tree.bind("<ButtonRelease-1>", self.select_record)
		
	def addRow(self):
		newCameraMaker = "New"
		newCameraModel = "Camera"
		camid = self.db.newCamera(newCameraMaker, newCameraModel)
		iid = self.iidFromCamLens(camid, 0)
		self.my_tree.insert(parent="", index='end', iid=iid, text='', values=(camid, newCameraMaker, newCameraModel))
		self.my_tree.see(iid)
		self.count += 1
	def addLens(self):
		newLensMaker = "New"
		newLensModel = "Lens"
		newLensLength=50
		newLensFstop=3.5
		cam=self.my_tree.focus()
		if (cam == ""):
			return
		camid = self.iidToCam(cam)
		lensid = self.db.newLens(camid, newLensMaker, newLensModel, newLensLength, newLensFstop)
		iid = self.iidFromCamLens(camid, lensid)
		self.my_tree.insert(parent=cam, index='end', iid=iid, text='', values=(lensid, "", "", newLensMaker, newLensModel, newLensLength, newLensFstop))
		self.my_tree.see(iid)
		self.count += 1
	def deleteRow(self):
		rowToDelete=self.my_tree.focus()
		if (rowToDelete == ""):
			return
		thisitem = self.my_tree.item(rowToDelete)
		vals = thisitem['values']
		if (self.rowIsLens(rowToDelete)):
			if askyesno(title="Delete", message=("Do you want to delete lens %s %s %s"%(vals[4], vals[5], vals[6]))):
				self.db.deleteLens(vals[0])
				self.my_tree.delete(rowToDelete)
		else:
			if askyesno(title="Delete", message=("Do you want to delete %s %s?"%(vals[1], vals[2]))):
				self.db.deleteCamera(vals[0])
				self.my_tree.delete(rowToDelete)
	def iidToCam(self, iid):
		return int(int(iid)/1000)
	def iidFromCamLens(self, cam, lens):
		return cam*1000+lens
	def rowIsLens(self, rowid):
		return (int(rowid) % 1000) > 0
	def colIsLens(self, column):
		return column > 2
	def setDesiredFiles(self, desired):
		self.desiredFiles = desired
	def onDoubleClick(self, event, row=None, col=None):
		''' Executed, when a row is double-clicked. Opens 
		EntryPopup above the item's column, so it is possible
		to select text '''
		
		# close previous popups
		# self.destroyPopups()

		# what row and column was clicked on
		if (row == None or col == None):
			rowid = self.my_tree.identify_row(event.y)
			column = self.my_tree.identify_column(event.x)
			column = int(column[1:])-1
			if (column < 1):
				return "break"
		else:
			rowid = row
			column = col
		if (self.rowIsLens(rowid) != self.colIsLens(column)):
			return "break"
		# get column position info
		x,y,width,height = self.my_tree.bbox(rowid, column=column)
		#### we have to figure out if this popup is on a camera or lens row, and not permit changes if it's in fields that ought to be blank
		# y-axis offset
		# pady = height // 2
		pady = 0

		# place Entry popup properly		 
		text = self.my_tree.set(rowid, column)
		self.entryPopup = EntryPopup(self, rowid, column, text)
		self.entryPopup.place( x=x, y=y+pady, width=width, height=height)
		return "break"
	def setInitialFocus(self, row):
		try:
			self.my_tree.selection_set(row)
			self.my_tree.focus(row)
			self.my_tree.see(row)
		except:
			return
	def getCurrentRowInfo(self):
		hasLens = False
		camInfoRow=self.my_tree.focus()
		if (camInfoRow == ""):
			camInfoRow = self.db.getstate("selected")
			showerror(title="Save camera information", message="Select a camera or lens for saving")
			return None
		thisitem = self.my_tree.item(camInfoRow)
		vals = thisitem['values']
		if (self.rowIsLens(camInfoRow)):
			hasLens = True
			if True:
				camid = self.iidFromCamLens(self.iidToCam(camInfoRow), 0)
				camItem = self.my_tree.item(camid)
				camvals = camItem['values']
				vals[1] = camvals[1]
				vals[2] = camvals[2]
			else:
				showerror(title="Save camera information", message="Can't successfully find the cam info for your lens %s %s"%(vals[4],vals[5]))
				raise ValueError
		return (hasLens, vals)
	def fileRequest(self, files):
		self.setDesiredFiles(files)
		self.textbox['text'] = "Unwritten files to be updated: %s%s"%("\n".join(files[:9]), "..." if len(files)>9 else "")
	def openFiles(self):
		self.openFilesFromSomeplace(None)
	def saveFiles(self):
		self.openFilesFromSomeplace(self.desiredFiles)
	def openFilesFromSomeplace(self, givenFiles):
		try:
			(hasLens, vals)=self.getCurrentRowInfo()
		except:
			return
		self.justStarted = False
		initialdir = self.db.getstate("dir")
		if (initialdir == None or len(initialdir) < 1):
			initialdir = os.path.expanduser("~")
		else:
			initialdir = initialdir[0]
		ft = ( 
			("Image files", ".jpg .jpeg .png .tif .tiff .gif"),
			("All files", ".*")
		)
		if ((givenFiles == None) or (len(givenFiles)<1)):
			givenFiles=filedialog.askopenfilenames(title="Save Camera Information To Files", initialdir=initialdir, multiple=True, filetypes=ft)
			if (len(givenFiles) == 0):
				return
			# remember the directory where we found one of these files so we can open it next time:
			pat = re.compile(r'.*(?=/)')
			initialdir = givenFiles[0]
			paths = pat.search(givenFiles[0])
			if (paths != None):
				initialdir = paths[0]
			self.db.setstate("dir", initialdir)
			# all remembered. 
		try:
			fl = float(vals[5])
		except:
			fl = 50
		try:
			ap = float(vals[6])
		except:
			ap = 3.5
		args=[self.exiftool,] 
		if (self.minorErrors.get() == 1):
			args.extend(["-m"])
		else:
			args.extend(["-overwrite_original_in_place"])
		args.extend([ "-Make="+vals[1], "-Model="+vals[2]])
		if (hasLens):
			args.extend(["-LensMake="+vals[3], "-LensModel="+vals[4], "-LensInfo=%f %f %f %f"%(fl, fl, ap, ap)])
		for i in givenFiles:
			args.extend([i])
		exifresults = subprocess.run(args, text=True, capture_output=True)
		if (exifresults.returncode != 0):
			showerror(title="exiftool results", message="Error %d\n %s"%( exifresults.returncode, exifresults.stderr))
			self.textbox['text']="Errors when updating %s"% ('\n'.join(givenFiles))
		else:
			self.textbox['text']="All files updated: %s%s"%("\n".join(givenFiles[:9]), "..." if len(givenFiles)>9 else "")

			
	def select_record(self, e):
		camInfoRow=self.my_tree.focus()
		self.db.setstate("selected", camInfoRow)
		pass

	def insert(self, cams, lens):
		lastparent=''
		self.count=0
		for cam in cams:
				camparent=self.my_tree.insert(parent="", index='end', iid=self.iidFromCamLens(cam[0], 0), text='', values=(cam[0], cam[1], cam[2]))
				self.count += 1
				for len in lens:
					if (len[1] == cam[0]):
						self.my_tree.insert(parent = camparent, index = 'end', iid = self.iidFromCamLens(cam[0], len[0]), text = '', values=(len[0], '', '', len[2], len[3], len[4], len[5]))
						self.count += 1
	def update_database_from_row(self, row):
		# do different things depending on whether this is a lens row or a camera row.
		
		thisitem = self.my_tree.item(row)
		vals = thisitem['values']
		if (self.rowIsLens(row)):
			self.db.updateLens(vals[0], vals[3], vals[4], vals[5], vals[6])
		else:
			self.db.updateCamera(vals[0], vals[1], vals[2])
#	
#		for record in records:
#				self.my_tree.insert(parent="", index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
#				count += 1

class EntryPopup(tkinter.Entry):

	def __init__(self, interactive, iid, col, text, **kw):
		''' If relwidth is set, then width is ignored '''
		parent = interactive.my_tree
		super().__init__(parent, **kw)
		self.tv = parent
		self.iid = iid
		self.col = col
		self.interactive = interactive

		self.insert(0, text) 
		# self['state'] = 'readonly'
		# self['readonlybackground'] = 'white'
		# self['selectbackground'] = '#1BA1E2'
		self['exportselection'] = False

		self.focus_force()
		self.select_all()
		self.bind("<Return>", self.on_return)
		self.bind("<Control-a>", self.select_all)
		self.bind("<Escape>", lambda *ignore: self.destroy())
		self.bind("<FocusOut>", self.on_return)
		self.bind("<Tab>", self.on_tab)

	def on_tab(self, event):
		self.tv.set(self.iid, self.col, self.get())
		interactive = self.interactive
		iid = self.iid
		col = self.col
		self.destroy()
		interactive.onDoubleClick(event, row=iid, col=col+1)
	def on_return(self, event):
		self.tv.set(self.iid, self.col, self.get())
		self.interactive.update_database_from_row(self.iid)
		self.destroy()

	def select_all(self, *ignore):
		''' Set selection on the whole text '''
		self.selection_range(0, 'end')

		# returns 'break' to interrupt default key-bindings
		return 'break'
