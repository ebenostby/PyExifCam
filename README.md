# PyExifCam
 Python code to maintain a camera database and apply to images with exiftool
 <h2>
What it is
 </h2>
 ExifCam is a tool to (a) maintain a camera and lens database (typically for film cameras), and (b) insert camera and lens information into image files. The database is
 kept in a sqlite file and can be edited within the ExifCam tool. Updating camera and lens information is done via an included copy of exiftool, which stores the
 information as exif tags. Currently, jpg, tif, png files are supported.
 <h2>
 Downloading ExifCam
 </h2>
 The app is saved as a zip file (at present) in the repository in a directory called <i>dist</i>
 Copy this and double-click on it to unzip (decompress) it. 
 I suspect you'll have to set security permissions on the Mac to let it run.
 Let me know how that works for you.
=======
 Installing exifcam
 </h2>
 There is an app file in the dist directory, stored as a zip file. Download this zip file, uncompress it, and move the resulting app file into your
 Applications directory or whereever you might want it.
 If you don't already have python3.9 or better installed, you will need that. 
 <a href="https://www.freecodecamp.org/news/python-version-on-mac-update/"> Here are some instructions on installing python 3.9 using homebrew.</a>
 Start exifcam by double-clicking on its icon, or by dragging-and-dropping image files onto the icon.
 <h2>
 Porting your camera information from AnalogExif
 </h2>
 On initial use, or whenever ExifCam doesn't find its camera database, it will look for and attempt to open an AnalogExif database. If it finds one, it will scan it and
 copy over camera and lens information. It doesn't handle any other information. AnalogExif doesn't normally maintain focal length information, so it looks in the lens 
 name string to see if there are values that look like focal length information. ExifCam mostly assumes lenses are fixed focal length, so zoom information is hamstrung.
 <h2>
Entering information into your database
 </h2>
 To enter a new camera name into your database, invoke Edit/New Camera (⌘N). A new row will be opened up, pre filled with "New" and "Camera" as maker and model names. 
 Edit these to suit. To edit a field, simply double-click on the field and type or edit. Hitting Tab will move you to the next field, and hitting Return will close the
 field. In either case, the database file is updated.
 To enter a new lens, first select a camera (or existing lens) and invoke Edit/New Lens (⌘L). The lens entered will be parented to the current camera. 
 <p>
 The camera database display can be sorted by clicking on a column header (click again to reverse order).
 <h2>
Saving camera information in your image files
 </h2>
 Once you have your camera information in the database, you can insert it into image files. Select a camera or a lens (which implicitly selects its parent camera).
 Then invoke File/Open-and-save (⌘O) and a dialog will appear. Select as many image files as you like. Hit the "open" button and ExifCam will insert the currently
 selected camera (and possibly lens) information into the images' exif tags. This is done by invoking a built-in copy of exiftool.
 <p>
 You can also drag and drop image files onto the program's icon. This will apply the currently selected camera (and lens) to the files you've chosen.
 However, if the program is not already open when you drop the files onto it, it will wait until you've selected a camera (and possibly a lens). The program will display
 a notice that it is waiting for you to save the files (<i>Unwritten files...</i>). To do so, invoke the File/Save (⌘S) command.  When files have been saved,
 the program always displays a notice saying <i>files updated:</i>.
 <p>
  The checkbox <i>Fix errors and save backup</i> is available to help prevent errors caused by exif tags that exiftool can't parse correctly. Normally this
  is an indication of an error in the image file. It will ask exiftool to reformat the tags to (hopefully) eliminate errors, and save the file
  as a backup copy before modifying it. I tick this box only when I've encountered errors in parsing the file, as otherwise I'd end up with a lot of backup copies.
  <h1>
   Code and copyright information
   </h1>
   
   Copyright 2022 Eben Ostby

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License. 
