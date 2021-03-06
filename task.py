"""Module containing a Task class"""


class Task:
    def __init__(self, note: str, tags=set(), date=None, reminders=[],
                 errors=[], whole_day=True):
        self.note = note
        self.tags = tags
        self.date = date
        self.reminders = reminders
        self.errors = errors

    def __str__(self):
        return self.note


if __name__ == "__main__":
    print(__doc__)
