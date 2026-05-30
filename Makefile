all:
	python3 -m PyInstaller exifcam.spec
	cd dist; rm -f exifcam.zip; zip -r exifcam.zip exifcam.app 
