import ftplib
from datetime import datetime, timedelta
import json

with open("./data/config.json") as file:
    data = json.load(file)
    FTP_HOST = data["FTP_HOST"]
    FTP_USER = data["FTP_USER"]
    FTP_PASS = data["FTP_PASS"]

ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
files = ftp.nlst()

with open("./data/last_modified.json") as file:
    last_modified_data = json.load(file)


period_signal = input(
    "Check if file hasn't been changed in the last day(d), hour(h), minute(m) or press enter if you only want to check if there is any change, no matter the duration: "
)
if period_signal == "d":
    period = int(input("How many days(1-30): "))
elif period_signal == "h":
    period = int(input("How many hours(1-23): "))
elif period_signal == "m":
    period = int(input("How many minutes(1-59): "))

def get_changed(files):
    changed_files = []
    for file_name in files:
        changed = False
        current_file_date = datetime.strptime(
            ftp.sendcmd(f"MDTM {file_name}").split()[-1], "%Y%m%d%H%M%S"
        )
        if period_signal == "":
            if last_modified_data[file_name] != current_file_date:
                print(f"{file_name} has changed")
                print(f"last changed: {last_modified_data[file_name]}")
                print(f"current change: {current_file_date}")
                data[file_name] = current_file_date
            else:
                print(f"{file_name} has not changed")
        else:
            last_modified_date = datetime.strptime(
                last_modified_data[file_name], "%Y-%m-%d %H:%M:%S"
            )
            if (
                current_file_date.day - last_modified_date.day > period
                and period_signal == "d"
            ):
                changed = True

            elif (
                current_file_date.hour - last_modified_date.hour > period
                and period_signal == "h"
            ):
                changed = True

            elif (
                current_file_date.minute - last_modified_date.minute > period
                and period_signal == "m"
            ):
                changed = True

            if changed:
                print(f"{file_name} has changed")
                print(f"last changed: {last_modified_data[file_name]}")
                print(f"current change: {current_file_date}")
                print(f"duration changed: within the last {period}{period_signal}")
                data[file_name] = current_file_date
                changed_files.append(file_name)
                changed = False
            else:
                print(f"{file_name} has not changed")

    return changed_files

changed_files = get_changed(files)
ftp.quit()

# import ftplib
# ftp = ftplib.FTP("0.0.0.0:2121", "farrel", "farrel123")
# ftp.mkd("changed_files")
# ftp.cwd("changed_files")

# for changed_file in changed_files:
#     with open(changed_file, "rb") as file:
#         # Use the FTP `storbinary` method to upload the file
#         ftp.storbinary(f"STOR {changed_file}", file)

# print(ftp.nlst())