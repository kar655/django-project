import subprocess

from .models import File, User, Directory


def init_database():
    user = User(login="login", name="name", password="password")
    user.save()
    directory = Directory(name="ROOT", description="Root directory", user_id=1)
    directory.save()
    return


def focus_on_program_elements_helper(file: File) -> str:
    result = subprocess.run(["frama-c", "-wp", "-wp-print", file.file_field.path],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    print(f"stdout = {result.stdout}")
    print(f"stderr = {result.stderr}")

    return result.stdout + result.stderr


def read_file(file: File) -> str:
    file.file_field.open("r")
    lines = file.file_field.read()
    file.file_field.close()
    return lines


def get_current_user(session) -> User:
    return User.objects.get(pk=session["uname_id"])
