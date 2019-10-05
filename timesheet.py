import os # used to check if files exist
import json # used to read / write json

class Timesheet(object):
    """Object for managing a timesheet.

    Saves records in a JSON file.
    """

    def __init__(self, args, filename):
        """Constructor,  initializes the class attributes.

        :param args: argparse.Namespace object
        :param str filename: The name of the JSON file
        """
        super(Timesheet, self).__init__()
        self.args = args
        self.filename = filename
        self.records = self.load_json_file()

    def add_record(self):
        """Add a new record in timesheet.
        """
        record = self.create_record()
        self.records.append(record)
        self.write_json_file(self.records)

    def create_record(self):
        """Create a record as dictionary.

        :param args: argparse.Namespace object
        :return: a dictionary with record data from argparse.Namespace object
        :rtype: dict
        """
        return {
            "date": self.args.date.strftime("%d.%m.%Y"),
            "start_day": self.args.work_hours[0].strftime("%H:%M"),
            "end_day": self.args.work_hours[1].strftime("%H:%M"),
            "start_break": self.args.break_time[0].strftime("%H:%M"),
            "end_break": self.args.break_time[1].strftime("%H:%M"),
            "comment": self.args.comment
        }

    def write_json_file(self, records):
        """Write list of records to JSON file.

        :param list records: list of records
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2)

    def load_json_file(self):
        """Load JSON file as list of records.
        Creates a file with an empty list if file doesn't exist.

        :return: list with records from file
        """
        if os.path.isfile(self.filename) and os.path.getsize(self.filename):
            with open(self.filename, "r", encoding='utf-8') as f:
                return json.load(f)
        else:
            self.write_json_file([])
            return []

    def record_exists(self, date):
        """Check if record exists already.

        :param date: datetime.date object
        return: a bool with the result
        """
        date = date.strftime("%d.%m.%Y")
        for record in self.records:
            if date == record["date"]:
                return True
        return False
