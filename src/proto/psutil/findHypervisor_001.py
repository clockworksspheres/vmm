import psutil
import re

for proc in psutil.process_iter(['pid', 'name']):
    print(f"{proc.info['pid']}: {proc.info['name']}")

#for proc in psutil.process_iter():
#    print(f"{proc.info}")

for proc in psutil.process_iter(['pid', 'name']):
    if re.match("^VMware Fusion$", proc.info['name']) or\
       re.match("^UTM$", proc.info['name']) or\
       re.match("^VirtualBox$", proc.info['name']):
        print(f"{proc.info['name']}")

