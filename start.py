import os
import sys

from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")


def run_server():
    execute_from_command_line(["manage.py", "runserver", "--noreload"])


if __name__ == "__main__":
    start = True
    if start:
        url_server = "172.28.178.81"
        # print(sys.argv[0])
        sys.argv[2] = sys.argv[2].replace("localhost", url_server)
    run_server()
