# SUSE Apprentices Timesheets made easy

## Contributions are welcome:
   + [ ] Adding "special" days like: vacation, school; only date and comment needed for that; 8h assumed for daily quota;
   + [ ] Method to fill in records from json file to xlsx exported file  
   + [ ] Method to create file names like `2019_10_eroca_timesheet.json` `2019_10_eroca_timesheet.xlsx` and implement where needed
   + [ ] Method to load specific json files of the given date's month and year


## Structure

+ Data is saved internally as `json` strings

+ Exports to `xlsx`, therefore: `pip install --user xlsxwriter`

## How it looks like
### Help
```
./azubi-timesheet.py --help
usage: azubi-timesheet [-v] [-n] [-d DD.MM.YYYY] [-w HH:MM-HH:MM]
                       [-b HH:MM-HH:MM] [-c COMMENT] [-h]
                       [add | delete | replace | export]

Keep track of your work hours. Add, delete, replace records. Export and print
at the end of the month!

positional arguments:
  add | delete | replace | export
                        Choose one of these subcommands.

optional arguments:
  -v, --version         Show program's version number and exit.
  -n, --non-interactive
                        Do not ask anything, use default answers
                        automatically.
  -d DD.MM.YYYY, --date DD.MM.YYYY
                        Date of the record.
  -w HH:MM-HH:MM, --work-hours HH:MM-HH:MM
                        Begin and end time of the work day.
  -b HH:MM-HH:MM, --break-time HH:MM-HH:MM
                        Begin and end time of the break.
  -c COMMENT, --comment COMMENT
                        Comment of the record, if needed.
  -h, --help            Show this help message and exit.
  ```

### Subcommands
+ `add` creates a new json string and appends it to the list
```
./azubi-timesheet.py add --date 07.10.2019 --work-hours 09:00-17:30 --break-time 12:00-12:30 --non-interactive
```

+ `replace` removes old record with same date, creates and appends a new one with the given data
```
./azubi-timesheet.py replace --date 07.10.2019 --work-hours 10:00-18:30 --break-time 13:00-13:30 --non-interactive
```

+ `delete` removes record with given date
```
./azubi-timesheet.py delete --date 07.10.2019
```

+ `export` creates an `xlsx` document
```
./azubi-timesheet.py export
```
