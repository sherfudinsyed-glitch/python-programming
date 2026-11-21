"""College Fest Registration package."""
class InvalidRecord(Exception):
    """Raised when a registration line is damaged or invalid."""


def read_lines(path):
    """Yield (line_number, line) one at a time (memory efficient)."""
    with open(path, "r", encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            line = line.strip()
            if line:                      # skip blank lines
                yield number, line


def parse_line(line):
    """'REG,Name,Dept,email,Event1;Event2' -> tuple of fields."""
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 5:
        raise InvalidRecord(f"expected 5 fields, found {len(parts)}")
    reg, name, dept, email, events = parts
    if not reg or not name or not dept:
        raise InvalidRecord("empty register number, name or department")
    event_list = [e.strip() for e in events.split(";") if e.strip()]
    if not event_list:
        raise InvalidRecord("no events chosen")
    return reg, name, dept, email, event_list
  from .reader import InvalidRecord


def is_valid_email(email):
    """Validate e-mail using string methods only."""
    if email.count("@") != 1 or " " in email:
        return False
    local, domain = email.split("@")
    if not local or not domain:
        return False
    if "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False
    return True


def validate_record(record):
    reg, name, dept, email, events = record
    if not is_valid_email(email):
        raise InvalidRecord(f"invalid e-mail '{email}'")
    return record
  import os


def write_master(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for reg, name, dept, email, events in records:
            f.write(f"{reg},{name},{dept},{email},{';'.join(events)}\n")


def write_event_files(folder, event_map):
    os.makedirs(folder, exist_ok=True)
    for event, students in event_map.items():
        safe = event.lower().replace(" ", "_")
        with open(os.path.join(folder, f"{safe}.txt"), "w", encoding="utf-8") as f:
            for reg, name in students:
                f.write(f"{reg},{name}\n")


def write_summary(path, total_read, valid, duplicates, errors, event_map):
    with open(path, "w", encoding="utf-8") as f:
        f.write("FEST REGISTRATION SUMMARY\n")
        f.write("=========================\n")
        f.write(f"Lines read        : {total_read}\n")
        f.write(f"Valid registrations: {valid}\n")
        f.write(f"Duplicates removed : {duplicates}\n")
        f.write(f"Rejected lines     : {errors}\n\n")
        f.write("Participants per event:\n")
        for event, students in sorted(event_map.items()):
            f.write(f"  {event}: {len(students)}\n")


def write_error_log(path, errors):
    with open(path, "w", encoding="utf-8") as f:
        for filename, line_no, message in errors:
            f.write(f"{filename} | line {line_no} | {message}\n")
          import os
import tempfile

from fest.reader import read_lines, parse_line, InvalidRecord
from fest.validator import validate_record
from fest.writer import (write_master, write_event_files,
                         write_summary, write_error_log)


def process(files, out_dir):
    seen = set()              # O(1) duplicate detection
    master = []
    event_map = {}
    errors = []
    total_read = 0
    duplicates = 0

    for path in files:
        name = os.path.basename(path)
        try:
            for line_no, line in read_lines(path):
                total_read += 1
                try:
                    record = validate_record(parse_line(line))
                except InvalidRecord as e:
                    errors.append((name, line_no, str(e)))
                    continue

                reg, student, dept, email, events = record
                if reg in seen:
                    duplicates += 1
                    errors.append((name, line_no, f"duplicate registration {reg}"))
                    continue

                seen.add(reg)
                master.append(record)
                for ev in events:
                    event_map.setdefault(ev, []).append((reg, student))

        except FileNotFoundError:
            errors.append((name, 0, "file not found"))
        except PermissionError:
            errors.append((name, 0, "permission denied"))
        except UnicodeDecodeError:
            errors.append((name, 0, "cannot decode file"))

    os.makedirs(out_dir, exist_ok=True)
    write_master(os.path.join(out_dir, "master.txt"), master)
    write_event_files(os.path.join(out_dir, "events"), event_map)
    write_summary(os.path.join(out_dir, "summary.txt"),
                  total_read, len(master), duplicates, len(errors), event_map)
    write_error_log(os.path.join(out_dir, "errors.log"), errors)
    return master, errors


if __name__ == "__main__":
    work = tempfile.mkdtemp()

    cse = os.path.join(work, "cse.txt")
    ece = os.path.join(work, "ece.txt")
    mech = os.path.join(work, "mech.txt")          # file that does NOT exist
    it = os.path.join(work, "it.txt")

    with open(cse, "w") as f:
        f.write("1001,Arun,CSE,arun@gmail.com,Dance;Singing\n"
                "1002,Bala,CSE,bala@gmail.com,Drama\n")
    with open(ece, "w") as f:
        f.write("1003,Charu,ECE,charu@gmail.com,Singing\n"
                "1001,Arun,CSE,arun@gmail.com,Dance\n"          # duplicate
                "1004,Dev,ECE,dev-at-gmail.com,Drama\n")        # invalid e-mail
    with open(it, "w") as f:
        f.write("1005,Esha,IT,esha@gmail.com,Dance\n"
                "1006,Farah,IT\n")                              # damaged line

    out = os.path.join(work, "output")
    master, errors = process([cse, ece, mech, it], out)

    print("MASTER LIST:")
    for r in master:
        print(" ", r)
    print("\nERROR LOG:")
    for e in errors:
        print(" ", e)
    print("\nSummary file:\n")
    print(open(os.path.join(out, "summary.txt")).read())
