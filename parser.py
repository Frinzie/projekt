"""Module that provides a parser function which takes a string
and returns a dictionary with the note, tags, date, reminders and errors"""

from task import Task
import datetime as dt
from dateutil.rrule import *

abbreviations = {
    "monday": MO, "mon": MO, "mo": MO,
    "tuesday": TU, "tue": TU, "tu": TU,
    "wednesday": WE, "wed": WE, "we": WE,
    "thursday": TH, "thu": TH, "th": TH,
    "friday": FR, "fri": FR, "fr": FR,
    "saturday": SA, "sat": SA, "sa": SA,
    "sunday": SU, "sun": SU, "su": SU
}

error_messages = {"!!ERROR": "Incorrect format; consult the docs",
                  "DMERROR": "Incorrect format; consult the docs",
                  "WPERROR": "Incorrect format; consult the docs",
                  "HMERROR": "Incorrect format; consult the docs",
                  "!ERROR": "Incorrect format; consult the docs",
                  "DRANGEERROR": "Incorrect format; consult the docs",
                  "MRANGEERROR": "Incorrect format; consult the docs"}

day_ranges = {1: range(1, 32), 2: range(1, 30), 3: range(1, 32),
              4: range(1, 31), 5: range(1, 32), 6: range(1, 31),
              7: range(1, 32), 8: range(1, 32), 9: range(1, 31),
              10: range(1, 32), 11: range(1, 31), 12: range(1, 32)}


def parser(text: str):
    note = ""
    tags = set()
    date = None
    errors = []
    for word in text.split():

        if word[0] == "#":
            tags.add(word[1:])
            continue

        elif word[0:2] == "!!":
            if word[2:].lower() in abbreviations:
                date = rrule(DAILY, dtstart=dt.date.today() +
                             dt.timedelta(days=1),
                             byweekday=abbreviations[word[2:].lower()])[0]
                continue
            errors.append((word, error_messages["!!ERROR"]))

        elif word[0] == "!":
            word_parts = word[1:].lower().split("h")
            month = None
            day = None
            hour = None
            minutes = None
            if len(word_parts) > 2:
                errors.append((word, error_messages["WPERROR"]))
            elif all(not w.isdigit() for w in word_parts):
                errors.append((word, error_messages["!ERROR"]))
            else:
                # Handles the DDMM part
                if len(word_parts[0]) in (1, 2):
                    day = int(word_parts[0])
                    if day not in range(1, 32):
                        errors.append((word, error_messages["DRANGEERROR"]))
                        note += word + " "
                        continue
                elif len(word_parts[0]) == 4:
                    day = int(word_parts[0][:2])
                    month = int(word_parts[0][2:])
                    if month not in range(1, 13):
                        errors.append((word, error_messages["MRANGEERROR"]))
                        note += word + " "
                        continue
                    if day not in day_ranges[month]:
                        errors.append((word, error_messages["DRANGEERROR"]))
                        note += word + " "
                        continue
                else:
                    errors.append((word, error_messages["DMERROR"]))
                    note += word + " "
                    continue
                # Handles the HHMM part (if needed)
                # if len(word_parts) == 2:
                #     if len(word_parts[1]) in (1, 2):
                #         hour = int(word_parts[1])
                #     elif len(word_parts[0]) == 4:
                #         hour = int(word_parts[1][:2])
                #         minutes = int(word_parts[1][2:])
                #     else:
                #         errors.append((word, error_messages["HMERROR"]))
                #     date_start = dt.datetime.now()
                # else:
                date_start = dt.date.today()
                date = rrule(DAILY, dtstart=date_start, bymonth=month,
                             bymonthday=day, byhour=hour, byminute=minutes)[0]
                continue

        note += word + " "
    return Task(note=note.strip(), tags=tags, date=date, errors=errors)


if __name__ == "__main__":
    print(__doc__)
    inp = None
    while 1:
        inp = input()
        if inp == "quit()":
            break
        x = parser(inp)
        print(x, x.tags, x.date, x.errors)
