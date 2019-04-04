import sys
import os, fnmatch
import array
from PIL import Image
import ntpath
import shutil
import errno

class CorruptImageDetective:
   search_path = ""
   corrupt_path = ""

   def __init__(self, sp, cp):
      self.corrupt_path = cp
      self.search_path = sp
   
   def find_files(self, directory, pattern):
      for root, dirs, files in os.walk(directory):
         for basename in files:
            for item in pattern:
               if fnmatch.fnmatch(basename, item):
                  filename = os.path.join(root, basename)
                  yield filename

   def check_files(self):
      for filepath in self.find_files(self.search_path, ['*.JPG', '*.JPEG', '*.jpg', '*.jpeg']):
         try:
            v_image = Image.open(filepath)
            v_image.verify()
         except:
            print ("Found corrupt image: " + filepath)
            filename = ntpath.basename(filepath)
            
            if not os.path.isdir(self.corrupt_path):
               try:
                  os.makedirs(self.corrupt_path)
               except OSError:
                  print("Error: Folder for corrupt image not created")
                  raise
            shutil.move(filepath, self.corrupt_path + filename)
            print ("Moved corrupt image to corrupt folder")


print ("Number of arguments:", len(sys.argv), "arguments.")
print ("Argument List:", str(sys.argv))

cid = CorruptImageDetective("/home/dima/Pictures/tmp", "/home/dima/Pictures/corrupt/")
cid.check_files()