import subprocess

from .models import File, User


def focus_on_program_elements_helper(file: File) -> str:
    result = subprocess.run(["frama-c", "-wp", "-wp-print", file.name],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    print(f"stdout = {result.stdout}")
    print(f"stderr = {result.stderr}")

    return result.stdout + result.stderr


def get_current_user(session) -> User:
    return User.objects.get(pk=session["uname_id"])
