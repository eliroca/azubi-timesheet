#!/usr/bin/env python3
#
# Copyright (c) 2019 Elisei Roca

"""
Keep track of your work hours. Add, delete, replace records.
Export and print at the end of the month!
"""

import sys
import re # used for regular expressions
import argparse # used to parse command line arguments
import datetime # used to save date and time objects
from timesheet import Timesheet

def execute(args):
    """Checks which subcommand was given and executes it.

    :param args: The namespace containing the scripts arguments
    :type args: :class:`argparse.Namespace`
    """
    timesheet = Timesheet(args, "json/timesheet.json")
    if args.subcommand == "add":
        if not timesheet.add_record():
            print("Exiting. Record already exists.")
            sys.exit(1)
    elif args.subcommand == "replace":
        if not timesheet.replace_record():
            print("Exiting. Record with given date not found.")
            sys.exit(1)
    elif args.subcommand == "delete":
        if not timesheet.delete_record():
            print("Exiting. Record with given date not found.")
            sys.exit(1)

def check_date(date, non_interactive, message, attempts=3):
    """Check that date respects format 'DD.MM.YYYY'.

    :param str date: The date supplied from the command line
    :param bool non_interactive: Tells the function if asking for user input is ok
    :param str message: Message to print when asking for date input
    :param int attempts: Allowed number of attempts to specify a valid date
    :return: Validated date object: date(year, month, day)
    :rtype: datetime.date
    """
    # Example of match dict: {'day': '3', 'month': '10', 'year': '2019'}
    regex = r'(?P<day>[0-9]{1,2})([\.,-])(?P<month>[0-9]{1,2})([\.,-])(?P<year>[0-9]{4})'
    if non_interactive:
        attempts = 1
    while attempts:
        if not date and not non_interactive:
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
            date = ""
            print("Expected date of following format: 'DD.MM.YYYY'")
    print("Exiting. You entered invalid date or didn't enter any input.")
    sys.exit(1)

def check_time_interval(time_interval, non_interactive, name="", attempts=3):
    """Check that time interval respects format 'HH:MM-HH:MM'.

    :param str time_interval: The time interval supplied from the command line
    :param bool non_interactive: Tells the function if asking for user input is ok
    :param str name: Name of time interval, used when printing to stdout
    :param int attempts: Allowed number of attempts to specify a valid time interval
    :return: Two validated time objects: time(hour, minute)
    :rtype: tuple(datetime.time, datetime.time)
    """
    # Example of match dict: {'start_hour': '09', 'start_minute': '00',
    #                         'end_hour': '17', 'end_minute': '30'}
    # Note: start_hour:start_minute take values from 00:00-23:59
    # whereas end_hour:end_minute    only    from    10:00-23:59
    # Can't decide if it's a bug or a feature...
    regex = r'(?P<start_hour>[0-9]|0[0-9]|1[0-9]|2[0-3])(:)' \
            '(?P<start_minute>[0-5][0-9])?([\-])' \
            '(?P<end_hour>1[0-9]|2[0-3])(:)' \
            '(?P<end_minute>[0-5][0-9])'
    if non_interactive:
        attempts = 1
    while attempts:
        if not time_interval and not non_interactive:
            time_interval = input("- Enter the BEGIN and END {}: ".format(name))
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
            time_interval = ""
            print("Expected {} of following format: 'HH:MM-HH:MM'".format(name))
    print("Exiting. You entered invalid {} or didn't enter any input.".format(name))
    sys.exit(1)

def check_args(args):
    """Checks if no arguments were given when running the script and asks for them.

    :param args: The namespace containing the scripts arguments
    :type args: :class:`argparse.Namespace`
    """
    # checking date
    args.date = check_date(args.date, args.non_interactive, "- Enter the DATE of record: ")
    if not args.subcommand == "delete":
        # checking work hours
        args.work_hours = check_time_interval(args.work_hours, args.non_interactive, "WORK HOURS")
        # checking break
        args.break_time = check_time_interval(args.break_time, args.non_interactive, "BREAK TIME")
        # checking comment
        if not args.comment and not args.non_interactive:
            args.comment=input("- Enter the COMMENT of record, if needed: ")

def parse_cli(args=None):
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result.

    :param list args: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result
    :rtype: :class:`argparse.Namespace`
    """
    parser=argparse.ArgumentParser(description=__doc__,
                                     prog="azubi-timesheet",
                                     add_help=False)
    parser.add_argument('-v', '--version',
                        action='version',
                        version="%(prog)s v0.1",
                        help="Show program's version number and exit."
                        )
    parser.add_argument(action='store',
                        dest="subcommand",
                        metavar="add | delete | replace",
                        choices=["add", "delete", "replace"],
                        nargs="?",
                        help="Choose one of these subcommands.",
                        )
    parser.add_argument("-n", "--non-interactive",
                        action='store_true',
                        dest="non_interactive",
                        help="Do not ask anything, use default answers automatically.",
                        )
    parser.add_argument("-d", "--date",
                        dest="date",
                        metavar="DD.MM.YYYY",
                        default="",
                        help="Date of the record.",
                        )
    parser.add_argument("-w", "--work-hours",
                        dest="work_hours",
                        metavar="HH:MM-HH:MM",
                        default="",
                        help="Begin and end time of the work day.",
                        )
    parser.add_argument("-b", "--break-time",
                        dest="break_time",
                        metavar="HH:MM-HH:MM",
                        default="",
                        help="Begin and end time of the break.",
                        )
    parser.add_argument("-c", "--comment",
                        dest="comment",
                        default="",
                        help="Comment of the record, if needed.",
                        )
    parser.add_argument("-h", "--help",
                        action="help",
                        default=argparse.SUPPRESS,
                        help="Show this help message and exit.",
                        )
    args = parser.parse_args(args)
    args.parser = parser
    # If no argument is given, print help info:
    if not sys.argv[1:]:
        parser.print_help()
        sys.exit(0)
    return args

def main(args=None):
    """Main function of the script.

    :param list args: a list of arguments (sys.argv[:1])
    """
    args = parse_cli(args)
    check_args(args)
    execute(args)
    return 0

if __name__ == "__main__":
    sys.exit(main())
