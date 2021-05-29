import re
import subprocess
from django.contrib.auth.models import User

from .models import File, Directory, FileSection


def init_root_directory(user: User):
    try:
        root_directory = user.directory_set.get(name="ROOT", user=user)
        root_directory.is_valid = True
        root_directory.save()
    except Directory.DoesNotExist:
        root_directory = Directory(name="ROOT", description="Root directory", user=user)
        root_directory.save()


def get_result(command: str):
    result = subprocess.run(command,
                            shell=True,
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    return result.stdout


def read_raw_file(file: File):
    with open(file.file_field.path) as f:
        content = f.read()
    return content


def focus_on_program_elements_helper(file: File):
    result = subprocess.run(["frama-c", "-wp", "-wp-print", file.file_field.path],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    line_tooltip = {}
    sections = []
    current = []
    line_number = None

    for line in result.stdout.splitlines(keepends=True):
        if re.match(r"-+", line):
            line_tooltip[line_number] = ''.join(current)
            current.append(line)
            sections.append((line_number, ''.join(current)))
            current = []
            line_number = None
        else:
            matches = re.search(r"line ([\d]+)", line)
            if matches is not None:
                line_number = int(matches.group(1))

            current.append(line)

    if len(current) > 0:
        sections.append((line_number, ''.join(current)))
        line_tooltip[line_number] = ''.join(current)

    return sections, line_tooltip

