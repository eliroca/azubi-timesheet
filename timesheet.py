import os # used to check if files exist
import json # used to read / write json

class Timesheet(object):
    """Object for managing a timesheet.

    Saves records in a JSON file.
    """

    def __init__(self, filename):
        super(Timesheet, self).__init__()
        self.filename = filename
