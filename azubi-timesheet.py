#!/usr/bin/env python3
#
# Copyright (c) 2019 Elisei Roca

"""
Keep track of your work hours. Add, edit, delete records.
Export and print at the end of the month!
"""
import sys
import re # used for regular expressions
import argparse # used to parse command line arguments
import datetime # used to save date and time objects

def check_date(date, message, attempts = 3):
    """Check that date respects format 'DD.MM.YYYY'.

    :param date: The date supplied from the command line
    :param message: Message to print when no date supplied
    :attempts: Allowed number of attempts to specify a valid date
    :return: Validated date object: date(year, month, day)
    :rtype: datetime.date
    """
    # Example of match dict: {'day': '3', 'month': '10', 'year': '2019'}
    regex = r'(?P<day>[0-9]{1,2})([\.,-])(?P<month>[0-9]{1,2})([\.,-])(?P<year>[0-9]{4})'
    while attempts:
        if not date:
            date = input(message)
        match = re.match(regex, date)
        if match:
            year = int(match.group("year"))
            month = int(match.group("month"))
            day = int(match.group("day"))
            date = datetime.date(year, month, day)
            return date
        else:
            attempts -= 1
            date = None
            print("Given date isn't valid.")
            print("Expected date of following format: 'DD.MM.YYYY'")
    print("Exiting. You entered invalid input too often.")
    sys.exit(1)

def check_time_interval(time_interval, message, attempts = 3):
    """Check that time interval respects format 'HH:MM-HH:MM'.

    :param time_interval: The time interval supplied from the command line
    :param message: Message to print when no time interval supplied
    :attempts: Allowed number of attempts to specify a valid time interval
    :return: Two validated time objects: time(hour, minute)
    :rtype: tuple(datetime.time, datetime.time)
    """
    # Example of match dict: {'start_hour': '09', 'start_minute': '00',
    #                         'end_hour': '17', 'end_minute': '30'}
    # Note: start_hour:start_minute take values from 00:00-23:59
    # whereas end_hour:end_minute    only    from    10:00-23:59
    # Can't decide if it's a bug or a feature...
    regex = r'(?P<start_hour>[0-9]|0[0-9]|1[0-9]|2[0-3])(:)?' \
            '(?P<start_minute>[0-5][0-9])?([\-])' \
            '(?P<end_hour>1[0-9]|2[0-3])(:)?' \
            '(?P<end_minute>[0-5][0-9])?'

    while attempts:
        if not time_interval:
            time_interval = input(message)
        match = re.match(regex, time_interval)
        if match:
            start_hour = int(match.group("start_hour"))
            start_minute = int(match.group("start_minute"))
            end_hour = int(match.group("end_hour"))
            end_minute = int(match.group("end_minute"))
            start_time = datetime.time(start_hour, start_minute)
            end_time = datetime.time(end_hour, end_minute)
            return start_time, end_time
        else:
            attempts -= 1
            time_interval = None
            print("Given time interval isn't valid.")
            print("Expected time interval of following format: 'HH:MM-HH:MM'")
    print("Exiting. You entered invalid input too often.")
    sys.exit(1)

def check_args(args):
    """Checks if no arguments were set when running the script and asks for them.

    :param args: The namespace containing the scripts arguments
    :type args: :class:`argparse.Namespace`
    """
    # checking date
    date_message = "- Enter the DATE of record: "
    args.date = check_date(args.date, date_message)
    # checking work hours
    work_hours_message = "- Enter the BEGIN and END of WORK DAY: "
    args.work_hours = check_time_interval(args.work_hours, work_hours_message)
    # checking break
    break_time_message = "- Enter the BEGIN and END of BREAK: "
    args.break_time = check_time_interval(args.break_time, break_time_message)
    # checking comment
    if not args.comment:
        args.comment = input("- Enter the COMMENT of record, if needed: ")

def parse_cli(args = None):
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result.

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result
    :rtype: :class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("-d", "--date",
                        dest = "date",
                        help = "date of record in format 'DD.MM.YYYY'",
                        )
    parser.add_argument("-w", "--work-hours",
                        dest = "work_hours",
                        help = "begin and end of work day in format 'HH:MM-HH:MM'",
                        )
    parser.add_argument("-b", "--break-time",
                        dest = "break_time",
                        help = "begin and end of break in format 'HH:MM-HH:MM'",
                        )
    parser.add_argument("-c", "--comment",
                        dest = "comment",
                        help = "comment of record, if needed",
                        )
    args = parser.parse_args(args)
    args.parser = parser
    # If no argument is given, print help info:
    if not sys.argv[1:]:
        parser.print_help()
        sys.exit(0)
    check_args(args)
    return args

def main(args=None):
    """main function of the script

    :param list args: a list of arguments (sys.args[:1])
    """
    args = parse_cli(args)
    return 0

if __name__ == "__main__":
    sys.exit(main())
