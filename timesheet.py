import os
import json
import xlsxwriter

class Timesheet(object):
    """Object for managing a timesheet.
    Saves records in a JSON file.
    """
    def __init__(self, args, records_file, export_file):
        """Constructor,  initializes the class attributes.

        :param args: argparse.Namespace object
        :param str records_file: The name of the JSON file
        :param str export_file: The name of the exported xlsx document
        """
        super(Timesheet, self).__init__()
        self.args = args
        json_dir = "json/"
        export_dir = "export/"
        if not os.path.isdir(json_dir):
            os.mkdir(json_dir)
        if not os.path.isdir(export_dir):
            os.mkdir(export_dir)
        self.records_file = os.path.join(json_dir + records_file)
        self.export_file = os.path.join(export_dir + export_file)

        self.records = self.load_json_file()

    def add_record(self):
        """Add a new record in timesheet.
        """
        if not self.record_exists(self.args.date):
            record = self.create_record()
            self.records.append(record)
            self.write_json_file(self.records)
            return True
        return False

    def delete_record(self):
        """Delete a record from timesheet.
        """
        date = self.args.date.strftime("%d.%m.%Y")
        for record in self.records:
            if date == record["date"]:
                self.records.remove(record)
                self.write_json_file(self.records)
                return True
        return False

    def replace_record(self):
        """Replace a record in timesheet.
        """
        date = self.args.date.strftime("%d.%m.%Y")
        for record in self.records:
            if date == record["date"]:
                if not record == self.create_record():
                    self.delete_record()
                    self.add_record()
                return True
        return False

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
        with open(self.records_file, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

    def load_json_file(self):
        """Load JSON file as list of records.
        Creates a file with an empty list if file doesn't exist.

        :return: list with records from file
        """
        if os.path.isfile(self.records_file) and os.path.getsize(self.records_file):
            with open(self.records_file, "r", encoding="utf-8") as f:
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

    def export(self):
        """Export timesheet as .xlsx file
        """
        workbook = xlsxwriter.Workbook(self.export_file)
        worksheet = workbook.add_worksheet()

        normal_format = workbook.add_format({"font_name": "Verdana", "align": "center", "valign": "vcenter"})
        title_format = workbook.add_format({"font_size": 16, "bold": True})

        #"bold": True, "border": True

        worksheet.set_column("A:A", 2.5)
        worksheet.set_column("L:L", 20)

        worksheet.merge_range("B5:K5", "Stundenzettel", title_format)
        worksheet.set_row(4, 25)

        worksheet.write("C7", "Name:", normal_format)
        worksheet.write("D7", "", normal_format)
        worksheet.write("C8", "Monat:", normal_format)
        worksheet.write("D8", "", normal_format)
        worksheet.merge_range("H8:I8", "Stundenübertrag", normal_format)
        worksheet.merge_range("J8:K8", "", normal_format)

        worksheet.write("C10", "Datum", normal_format)
        worksheet.write("D10", "Kommt", normal_format)
        worksheet.write("E10", "Geht", normal_format)
        worksheet.write("F10", "P-Beginn", normal_format)
        worksheet.write("G10", "P-Ende", normal_format)
        worksheet.write("H10", "Pause", normal_format)
        worksheet.write("I10", "AZ", normal_format)
        worksheet.merge_range("J10:K10", "GES-Stunden", normal_format)
        worksheet.write("L10", "Kommentar", normal_format)


        worksheet.merge_range("H35:I35", "Stundenübertrag", normal_format)
        worksheet.merge_range("J35:K35", "", normal_format)

        worksheet.write("C39", "Soll:")
        worksheet.write("H39", "Gesamt:")


        worksheet.write("C42", "Unterschrift Auszubildender")
        worksheet.write("G42", "Unterschrift Betreuer")
        worksheet.write("K42", "Unterschrift Ausbilder")

        worksheet.write("C44", "____________________")
        worksheet.write("G44", "____________________")
        worksheet.write("K44", "____________________")

        workbook.close()
        return True
