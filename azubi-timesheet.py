#!/usr/bin/env python3
#
# Copyright (c) 2019 Elisei Roca

"""
Keep track of your work hours. Add, edit, delete records.
Export and print at the end of the month!
"""
import sys
import argparse

def parse_cli(cliargs=None):
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result.

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result
    :rtype: :class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-d", "--date",
                        dest="date",
                        help="Date of record in format 'DD.MM.YY'.",
                        )
    parser.add_argument("-w", "--work-hours",
                        dest="work_hours",
                        help="Begin and end of work day in format 'HH:MM-HH:MM'.",
                        )
    parser.add_argument("-b", "--break-time",
                        dest="break_time",
                        help="Begin and end of break in format 'HH:MM-HH:MM'.",
                        )
    parser.add_argument("-c", "--comment",
                        dest="comment",
                        help="Comment for record, if needed.",
                        )
    args = parser.parse_args(args=cliargs)
    #check_args(args)
    return args

if __name__ == "__main__":
    args = parse_cli()
    print("{}, {}, {}, {}".format(args.date, args.work_hours, args.break_time, args.comment))
    sys.exit(0)
