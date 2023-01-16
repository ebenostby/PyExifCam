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

def BuildMenus(root, inter, saveablefiles):
	# Add Menu
	my_menu = tkinter.Menu(root)
	root.config(menu=my_menu)



	# Configure our menu
	file_menu = tkinter.Menu(my_menu, tearoff=0)
	my_menu.add_cascade(label="File", menu=file_menu)
	# Drop down menu
	if (saveablefiles):
		file_menu.add_command(label="Save", command=inter.saveFiles, accelerator="Command-S")
		root.bind_all("<Command-s>", lambda event:inter.saveFiles())
	file_menu.add_command(label="Open-and-save", command=inter.openFiles, accelerator="Command-O")
	root.bind_all("<Command-o>", lambda event:inter.openFiles())

	#Search Menu
	edit_menu = tkinter.Menu(my_menu, tearoff=0)
	my_menu.add_cascade(label="Edit", menu=edit_menu)
	# Drop down menu
	edit_menu.add_command(label="New Camera", command=inter.addRow, accelerator="Command-N")
	root.bind_all("<Command-n>", lambda event:inter.addRow())
	edit_menu.add_command(label="New Lens", command=inter.addLens, accelerator="Command-L")
	root.bind_all("<Command-l>", lambda event:inter.addLens())

	edit_menu.add_command(label="Delete", command=inter.deleteRow, accelerator="Command-D")
	root.bind_all("<Command-d>", lambda event:inter.deleteRow())
	edit_menu.add_separator()
