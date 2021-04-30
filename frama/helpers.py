import re
import subprocess

from .models import File, User, Directory, FileSection


def init_database():
    user = User(login="login", name="name", password="password")
    user.save()
    directory = Directory(name="ROOT", description="Root directory", user_id=1)
    directory.save()
    return


def get_result(command: str):
    result = subprocess.run(command,
                            shell=True,
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    return result.stdout


def focus_on_program_elements_helper(file: File):
    result = subprocess.run(["frama-c", "-wp", "-wp-print", file.file_field.path],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    def parse_between_dashed_lines(process_output: str):
        line_tooltip = {}
        parsed = []
        current = []
        line_number = None

        for line in process_output.splitlines(keepends=True):
            if re.match(r"-+", line):
                parsed.append((line_number, ''.join(current)))
                line_tooltip[line_number] = ''.join(current)
                current = []
                line_number = None
            else:
                matches = re.search(r"line ([\d]+)", line)
                if matches is not None:
                    line_number = int(matches.group(1))

                current.append(line)

        if len(current) > 0:
            parsed.append((line_number, ''.join(current)))
            line_tooltip[line_number] = ''.join(current)

        return line_tooltip

    parsed = parse_between_dashed_lines(result.stdout)

    return result.stdout + result.stderr, parsed


def read_file(file: File):
    sections = {
        "predicate": FileSection.SectionCategory.PROCEDURE,
        "requires": FileSection.SectionCategory.PRECONDITION,
        "ensures": FileSection.SectionCategory.POSTCONDITION,
        "assert": FileSection.SectionCategory.ASSERTION,
        "lemma": FileSection.SectionCategory.LEMMA,
        "loop": FileSection.SectionCategory.INVARIANT
    }

    file.file_field.open("r")

    result = []
    for line in file.file_field.readlines():
        match_results = re.search(r"@ +([a-z]+)", line)
        if match_results is not None:
            match = match_results.group(1)
            if match in sections:
                result.append((sections[match], line))
                continue

        result.append((None, line))

    file.file_field.close()
    return result


def get_current_user(session) -> User:
    return User.objects.get(pk=session["uname_id"])
