#!/usr/bin/python

import os
import time
import shutil

now = time.time()
num_of_days = 86400 * 7 # 7 is the number of days and can be changed
disk = os.statvfs("/home/pi/motion_camera/recorded_video/")

totalBytes = float(disk.f_bsize*disk.f_blocks)
bytesUsed = float(disk.f_bsize*(disk.f_blocks-disk.f_bfree))

# os.system(rsync avr -e ssh /home/pi/motion_camera/recorded_video/ pi@192.168.xxx.xxx):/destination/path


## if the percentage of bytes used is greater than 90% of the total
## space, remove all directories older than one week
if (bytesUsed / totalBytes > .9):
  dir_to_search = "/home/pi/motion_camera/recorded_video/"
  for root, dirnames, filenames in os.walk(dir_to_search):
    for dir in dirnames:
      timestamp = os.path.getmtime(os.path.join(root,dir))
      if now - num_of_days > timestamp:
        shutil.rmtree(os.path.join(root,dir))
        
        
