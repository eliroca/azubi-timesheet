#!/usr/bin/env python3
#
# Copyright (c) 2019 Elisei Roca

"""
Keep track of your work hours. Add, edit, delete records.
Export and print at the end of the month!
"""
import sys
import argparse

def parse_cli(args=None):
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result.

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result
    :rtype: :class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-d", "--date",
                        dest="date",
                        help="date of record in format 'DD.MM.YY'",
                        )
    parser.add_argument("-w", "--work-hours",
                        dest="work_hours",
                        help="begin and end of work day in format 'HH:MM-HH:MM'",
                        )
    parser.add_argument("-b", "--break-time",
                        dest="break_time",
                        help="begin and end of break in format 'HH:MM-HH:MM'",
                        )
    parser.add_argument("-c", "--comment",
                        dest="comment",
                        help="comment of record, if needed",
                        )
    args = parser.parse_args(args)
    #check_args(args) # TODO: implement checks
    args.parser = parser
    # If no argument is given, print help info:
    if not sys.argv[1:]:
        parser.print_help()
        sys.exit(0)
    return args

def main(args=None):
    """main function of the script

    :param list args: a list of arguments (sys.args[:1])
    """
    args = parse_cli(args)
    print("{}, {}, {}, {}".format(args.date, args.work_hours, args.break_time, args.comment))
    return 0

if __name__ == "__main__":
    sys.exit(main())
