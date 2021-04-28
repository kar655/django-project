import re
from pprint import pprint
import subprocess

from .models import File, User, Directory, FileSection


def init_database():
    user = User(login="login", name="name", password="password")
    user.save()
    directory = Directory(name="ROOT", description="Root directory", user_id=1)
    directory.save()
    return


def get_result(file: File):
    result = subprocess.run(["frama-c", "-wp", "-wp-log=r:result.txt", file.file_field.path],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    print("get_result stdout =====")
    print(result.stdout)
    print("get_result stderr =====")
    print(result.stderr)

    return result.stdout, result.stderr


def focus_on_program_elements_helper(file: File) -> str:
    result = subprocess.run(["frama-c", "-wp", "-wp-print", file.file_field.path],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    # print(f"stdout = {result.stdout}")
    # print(f"stderr = {result.stderr}")
    #
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
                    print(f"============LINE NUMBER = {line_number}")

                current.append(line)

        if len(current) > 0:
            parsed.append((line_number, ''.join(current)))
            line_tooltip[line_number] = ''.join(current)

        pprint(line_tooltip)

        return line_tooltip
        # return parsed

    parsed = parse_between_dashed_lines(result.stdout)
    pprint(parsed)
    # for section in parsed:
    #     print("SECTION:")
    #     print(section)

    return result.stdout + result.stderr, parsed
    # return result.stdout + result.stderr


def read_file(file: File) -> str:
    #         PROCEDURE = "Procedure", gettext_lazy("Procedure")
    #         PROPERTY = "Property", gettext_lazy("Property")
    #         LEMMA = "Lemma", gettext_lazy("Lemma")
    #         ASSERTION = "Assertion", gettext_lazy("Assertion")
    #         INVARIANT = "Invariant", gettext_lazy("Invariant")
    #         PRECONDITION = "Precondition", gettext_lazy("Precondition")
    #         POSTCONDITION = "Postcondition", gettext_lazy("Postcondition")
    sections = {
        "predicate": FileSection.SectionCategory.PROCEDURE,
        "requires": FileSection.SectionCategory.PRECONDITION,
        "ensures": FileSection.SectionCategory.POSTCONDITION,
        "assert": FileSection.SectionCategory.ASSERTION,
        "lemma": FileSection.SectionCategory.LEMMA,
        "loop invariant": FileSection.SectionCategory.INVARIANT
        # "logic real": FileSection.SectionCategory
    }

    file.file_field.open("r")
    # lines = file.file_field.read()
    lines = "EMPTY"

    result = []
    for line in file.file_field.readlines():
        match_results = re.search(r"@ +([a-z]+(?: [a-z]+)?)", line)
        if match_results is not None:
            match = match_results.group(1)
            if match in sections:
                result.append((sections[match], line))
            else:
                result.append((None, line))
        else:
            result.append((None, line))

    file.file_field.close()
    # pprint(result)
    return result


def get_current_user(session) -> User:
    return User.objects.get(pk=session["uname_id"])
