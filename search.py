import os, fnmatch
import array
from PIL import Image
import ntpath
import shutil


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            for item in pattern:
               if fnmatch.fnmatch(basename, item):
                   filename = os.path.join(root, basename)
                   yield filename


for filepath in find_files('/media/nfs/pictures', ['*.JPG', '*.JPEG', '*.jpg', '*.jpeg']):
    print 'Found picture:', filepath
    try:
       v_image = Image.open(filepath)
       v_image.verify()
    except:
       print "Unexpected error:", filepath
       filename = ntpath.basename(filepath)
       shutil.move(filepath, "/home/dima/Pictures/corrupt/" + filename)
