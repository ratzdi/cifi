# MIT License
# 
# Copyright (c) 2019 Dimitri Ratz
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

import sys
import os
import fnmatch
import ntpath
import shutil
from PIL import Image
import argparse

class CorruptImageDetective:
    search_path = ""
    corrupt_path = ""
    corrupt_file_counter = 0

    def __init__(self, sp, cp):
        self.corrupt_path = cp
        self.search_path = sp

    def findfiles(self, directory, pattern):
        for root, dirs, files in os.walk(directory):
            for basename in files:
                for item in pattern:
                    if fnmatch.fnmatch(basename, item):
                        filename = os.path.join(root, basename)
                        yield filename

    def checkfiles(self):
        print("Start checking files on ", self.search_path)
        for filepath in self.findfiles(self.search_path, ['*.JPG', '*.JPEG', '*.jpg', '*.jpeg']):
            try:
                img = Image.open(filepath)
                img.verify()
            except:
                print ("Found corrupt image: " + filepath)
                self.corrupt_file_counter += self.corrupt_file_counter
                filename = ntpath.basename(filepath)
                if not os.path.isdir(self.corrupt_path):
                    try:
                        os.makedirs(self.corrupt_path)
                    except OSError:
                        print("Error: Folder for corrupt image not created")
                        raise
                shutil.copyfile(filepath, os.path.join(self.corrupt_path, filename))
                print ("Moved corrupt image.")


parser = argparse.ArgumentParser(description="cifi - corrupt image finder", 
                    usage="%(prog)s -s search/path -t target/path")
parser.add_argument("-s", dest="search_path", type=str, required=True,
                    help="Search path where from start search.")
parser.add_argument("-t", dest="target_path", type=str, required=True,
                    help="Target path to move corrupt files.")

args = parser.parse_args()

if os.path.exists(args.search_path) & os.path.exists(args.target_path):
     cid = CorruptImageDetective(args.search_path, args.target_path)
     cid.checkfiles()
     print("Searching finished.")
     print("Corrupt files found:", cid.corrupt_file_counter)
