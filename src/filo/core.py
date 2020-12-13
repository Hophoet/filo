#
import os
import time
import datetime
import logging
#
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler

class LHandler(LoggingEventHandler):
	#constructor
	def __init__(self, tracked_folder):
		super(LHandler, self).__init__()
		self.tracked_folder = tracked_folder
		self.logger = logging.root
	def on_moved(self, event):
		what = 'directory' if event.is_directory else 'file'
		self.logger.info("Moved %s: from %s to %s", what, event.src_path, event.dest_path)
		time = str(datetime.datetime.now())
		print(dir(event))
		print(f"{time} Moved {what}: from {event.src_path} to {event.dest_path}")

#file handle custom class
class FHandler(FileSystemEventHandler):
	#constructor
	def __init__(self, folder_to_track, files_destination, directories_destination):
		super(FHandler, self).__init__()
		self.folder_to_track = folder_to_track
		self.files_destination = files_destination
		self.directories_destination = directories_destination

	#on modified event method
	def on_modified(self, event):
		#
		for filename in os.listdir(self.folder_to_track):
			#build the file absolute path
			abspath = os.path.join(event.src_path, filename)
			#files case
			if(os.path.isfile(abspath)):
				#files destination exists case
				if(os.path.exists(self.files_destination)):
					#moving to the destination
					os.rename(abspath,  self.files_destination+'/'+filename)
				#files destination not exists case
				else:
					#creation of the destination before the moving
					os.mkdir(self.files_destination)
					os.rename(abspath,  self.files_destination+'/'+filename)
			
			#directories case
			if(os.path.isdir(abspath)):
				#directories destination exists case
				if abspath != self.files_destination and abspath != self.directories_destination:
					#directories destination exists case
					if(os.path.exists(self.directories_destination)):
						#moving to the destination
						os.rename(abspath,  self.directories_destination+'/'+filename)
					#directories destination not exists case
					else:
						#destination creation before the moving
						os.mkdir(self.directories_destination)
						os.rename(abspath,  self.directories_destination+'/'+filename)
	


#file management class
class FileM:
	""" File management """
	def __init__(self, tracked_directory, files_destination, directories_destination):
		self.tracked_directory = tracked_directory
		self.files_destination = files_destination
		self.directories_destination = directories_destination
		self.event_handler = FHandler(tracked_directory, files_destination, directories_destination)
		self.log_handler = LHandler(tracked_directory)
		self.observer = Observer()

	#run method
	def run(self):
		#set of the event listener
		self.observer.schedule(self.event_handler, self.tracked_directory, recursive=True)
		self.observer.schedule(self.log_handler, self.tracked_directory, recursive=True)
		self.observer.start()
		try:
			#listener with loop
			while True:
				time.sleep(10)
		#cancel the listener on keyborder interruption
		except KeyboardInterrupt:
			self.observer.stop()
		self.observer.join()



