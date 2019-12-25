#!/usr/bin/env python3
#
# Copyright (c) 2019 Elisei Roca
#
"""
Keep track of your work hours. Add, delete, update records.
Export and print at the end of the month!
"""

import os
import sys
import argparse
import datetime
from .timesheet import Timesheet

__author__ = "Elisei Roca"
__version__ = "0.9"
__prog__ = os.path.basename(sys.argv[0])

def execute(args):
    """Checks which subcommand was given and executes it.

    :param args: The namespace containing the scripts arguments
    :type args: :class:`argparse.Namespace`
    """
    timesheet = Timesheet()
    if args.subcommand == "add":
        if not timesheet.add_record(args.date, args.work_hours, args.break_time, args.comment, args.special):
            print("Exiting. Record already exists.")
            sys.exit(1)
    elif args.subcommand == "update":
        if not timesheet.update_record(args.date, args.work_hours, args.break_time, args.comment, args.special):
            print("Exiting. Record with given date not found.")
            sys.exit(1)
    elif args.subcommand == "delete":
        if not timesheet.delete_record(args.date):
            print("Exiting. Record with given date not found.")
            sys.exit(1)
    elif args.subcommand == "export":
        if not timesheet.export(args.date):
            print("Exiting. No idea why yet.")
            sys.exit(1)
    elif args.list_config:
        timesheet.list_config()
    elif args.set_config:
        key, value = (item.strip() for item in args.set_config.split("="))
        if not timesheet.set_config(key, value):
            print("Exiting. Given key '{}' cannot be configured.".format(key))
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
    if non_interactive:
        attempts = 1
    while attempts:
        if not date and not non_interactive:
            date = input(message)
        try:
            date = datetime.datetime.strptime(date, "%d.%m.%Y")
            return date
        except ValueError:
            print("Expected date of following format: 'DD.MM.YYYY'",
                  file=sys.stderr)
        attempts -= 1
        date = ""
    print("Exiting. You entered invalid date or didn't enter any input.",
          file=sys.stderr)
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
    if non_interactive:
        attempts = 1
    while attempts:
        if not time_interval and not non_interactive:
            time_interval = input("- Enter the BEGIN and END of {}: ".format(name))
        try:
            start, end = time_interval.split("-")
            start = datetime.datetime.strptime(start, "%H:%M")
            end = datetime.datetime.strptime(end, "%H:%M")
            return start.time(), end.time()
        except ValueError:
            print("Expected {} of following format: 'HH:MM-HH:MM'".format(name),
                  file=sys.stderr)
        attempts -= 1
        time_interval = ""
    print("Exiting. You entered invalid {} or didn't enter any input.".format(name),
          file=sys.stderr)
    sys.exit(1)

def check_args(args):
    """Checks if no arguments were given when running the script and asks for them.

    :param args: The namespace containing the scripts arguments
    :type args: :class:`argparse.Namespace`
    """
    if not args.subcommand == "config":
        # checking date
        args.date = check_date(args.date, args.non_interactive, "- Enter the DATE of record: ")
        if not args.subcommand in ["delete", "export"]:
            # checking comment
            if not args.comment and not args.non_interactive:
                args.comment=input("- Enter the COMMENT of record, if needed: ")
            if not args.special:
                # checking work hours
                args.work_hours = check_time_interval(args.work_hours, args.non_interactive, "WORK HOURS")
                # checking break
                args.break_time = check_time_interval(args.break_time, args.non_interactive, "BREAK TIME")
            else:
                args.work_hours = (datetime.time(0, 0), datetime.time(0, 0))
                args.break_time = (datetime.time(0, 0), datetime.time(0, 0))

def parse_cli(args=None):
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result.

    :param list args: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result
    :rtype: :class:`argparse.Namespace`
    """
    parser=argparse.ArgumentParser(description=__doc__,
                                   prog=__prog__,
                                   epilog="Type <SUBCOMMAND> --help for more info.",
                                   add_help=False)
    global_args = parser.add_argument_group('global arguments')
    global_args.add_argument("-h", "--help",
                             action="help",
                             help=argparse.SUPPRESS)
    global_args.add_argument("-V", "--version",
                             action="version",
                             version="%(prog)s {}".format(__version__),
                             help="show program's version number and exit")
    global_args.add_argument("-n", "--non-interactive",
                             action="store_true",
                             dest="non_interactive",
                             help="do not ask anything, use default answers automatically")
    # parser with basic settings
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument("-h", "--help",
                            action="help",
                            help=argparse.SUPPRESS)
    # parser with minimal arguments
    min_parser = argparse.ArgumentParser(add_help=False,parents=[base_parser])
    min_parser.add_argument("-d", "--date",
                            dest="date",
                            metavar="DD.MM.YYYY",
                            default="",
                            help="date of the record")
    # parser with extended arguments
    ext_parser = argparse.ArgumentParser(add_help=False,parents=[min_parser])
    ext_parser.add_argument("-w", "--work-hours",
                            dest="work_hours",
                            metavar="HH:MM-HH:MM",
                            default="",
                            help="begin and end time of the work day")
    ext_parser.add_argument("-b", "--break-time",
                            dest="break_time",
                            metavar="HH:MM-HH:MM",
                            default="",
                            help="begin and end time of the break")
    ext_parser.add_argument("-c", "--comment",
                            dest="comment",
                            default="",
                            help="comment of the record, if needed")
    ext_parser.add_argument("-s", "--special-record",
                            action="store_true",
                            dest="special",
                            help="special records only need a date and a comment")

    subparsers = parser.add_subparsers(title="available subcommands",
                                       dest="subcommand",
                                       metavar="<SUBCOMMAND>")
    # subparser for 'add' subcommand:
    parser_add = subparsers.add_parser("add",
                                       description=("Add a new record."),
                                       help="add a new record",
                                       add_help=False,
                                       parents=[ext_parser])
    # subparser for 'update' subcommand:
    parser_update = subparsers.add_parser("update",
                                          description=("Update an existing record."),
                                          help="update an existing record",
                                          add_help=False,
                                          parents=[ext_parser])
    # subparser for 'delete' subcommand:
    parser_delete = subparsers.add_parser("delete",
                                          description=("Delete a record."),
                                          help="delete an existing record",
                                          add_help=False,
                                          parents=[min_parser])
    # subparser for 'export' subcommand:
    parser_export = subparsers.add_parser("export",
                                          description=("Export records of a month as .xlxs file."),
                                          help="export records as .xlsx file",
                                          add_help=False,
                                          parents=[min_parser])
    # subparser for 'config' subcommand:
    parser_config = subparsers.add_parser("config",
                                          description=("Configure the app with key=value pairs"),
                                          help="configure the app with key=value pairs",
                                          add_help=False,
                                          parents=[base_parser])
    config_args = parser_config.add_mutually_exclusive_group()
    config_args.add_argument("--set",
                               dest="set_config",
                               metavar="key=value",
                               default="",
                               help="enter a key=value pair configuration")
    config_args.add_argument("--list",
                             action="store_true",
                             dest="list_config",
                             help="see the app's configuration")
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
