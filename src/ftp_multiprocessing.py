import ftplib
from multiprocessing import Process
import time
import os, json
import logging

time_now = time.time()

# setting up logger
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


# loading config file
with open("./data/config.json") as file:
    data = json.load(file)
    FTP_HOST = data["FTP_HOST"]
    FTP_USER = data["FTP_USER"]
    FTP_PASS = data["FTP_PASS"]
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)


def download_file(file):
    """Download a file from the FTP server"""
    with open(file, "wb") as f:
        ftp.retrbinary("RETR " + file, f.write)
        logging.info(f"{f} is written")


def main():
    """Download all files from the FTP server in parallel"""
    files = ftp.nlst()
    processes = [Process(target=download_file, args=(file,)) for file in files]
    for process in processes:
        process.start()
    for process in processes:
        process.join()


if __name__ == "__main__":
    main()
    logging.info(f"Time taken: {time.time() - time_now} seconds")
    os.startfile(".")   
