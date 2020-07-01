# https://blog.magrathealabs.com/filesystem-events-monitoring-with-python-9f5329b651c3
# Filesystem events monitoring with Python


# https://pypi.org/project/watchdog/
# Collecting watchdog
#   Downloading watchdog-0.10.2.tar.gz (95 kB)
#      |UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU| 95 kB 1.1 MB/s
# Collecting pathtools>=0.1.1
#   Downloading pathtools-0.1.2.tar.gz (11 kB)
# Using legacy setup.py install for watchdog, since package 'wheel' is not installed.
# Using legacy setup.py install for pathtools, since package 'wheel' is not installed.
# Installing collected packages: pathtools, watchdog
#     Running setup.py install for pathtools ... done
#     Running setup.py install for watchdog ... done
# Successfully installed pathtools-0.1.2 watchdog-0.10.2
# PS C:\Users\JF30LB\Projects\aws-lambda-port-check-master> 
import os
import logging
import sys
import time

from Tools import tools_v000 as tools
from AM import am as am
from os.path import dirname
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler


# -7 for the name of this project Sniffer
save_path = dirname(__file__)[ : -7]
propertiesFolder_path = save_path + "Properties"

path_to_look = tools.readProperty(propertiesFolder_path, 'Sniffer', 'path_to_look=')

class Event(FileSystemEventHandler):
    def on_created(self, event):
        what = 'directory' if event.is_directory else 'file'
        if what == 'file' :
            logging.info("One %s: this is the location : %s", what, event.src_path)
            am.launchProcess(event.src_path)
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else path_to_look
    event_handler = Event()

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()