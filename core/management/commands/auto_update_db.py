# get a folder and get the filepaths of all the csv files in it.

import glob
import os
import time

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileUpdateHandler(FileSystemEventHandler):
    def __init__(self, csv_files) -> None:
        self.csv_files = csv_files

    def on_modified(self, event):
        # this method is called by default, when there is a change in the folder.
        if not event.is_directory:
            call_command("data_intake", self.csv_files)


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("tracked_folder")

    def handle(self, *args, **kwargs):
        # change the curent working directory to the tracked folder.
        tracked_folder = kwargs["tracked_folder"]
        csv_files = glob.glob(os.path.join(tracked_folder, "*.csv"))

        # instantiate the event handler
        event_handler = FileUpdateHandler(csv_files)

        # Create an observer to monitor the folder
        observer = Observer()
        observer.schedule(event_handler, path=tracked_folder, recursive=True)
        observer.start()

        try:
            print(f"Monitoring folder: {tracked_folder}")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
