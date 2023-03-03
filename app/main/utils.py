import datetime
import os

from flask import current_app


def log_data(data, dir_name=None, filename=datetime.date.today().day, logrotate=True):
    if logrotate:
        dir = os.path.join(
            current_app.root_path,
            "logs",
            str(datetime.datetime.now().year),
            str(datetime.datetime.now().month),
        )
        if dir_name:
            dir = os.path.join(
                current_app.root_path,
                "logs",
                dir_name,
                str(datetime.datetime.now().year),
                str(datetime.datetime.now().month),
            )
    else:
        dir = os.path.join(current_app.root_path, "logs")
        if dir_name:
            dir = os.path.join(current_app.root_path, "logs", dir_name)

    if not os.path.exists(dir):
        os.makedirs(dir)

    dd = datetime.date.today().day
    file_path = os.path.join(dir, str(dd) + ".log")

    with open(file_path, "a") as _file:
        tab_char = "\t"
        newline_char = "\n"
        log_str = f"{datetime.datetime.now()}{tab_char}{data}{newline_char}"
        status = _file.write(log_str)
        return True
