import concurrent.futures
import ftplib
import time
import json
import logging
import os
import sys

# setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./output.log')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] - %(funcName)s - %(message)s',datefmt='%a, %d %b %Y %H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

logging.info("getting configurations from config file")
with open("./data/config.json") as file:
    data = json.load(file)
    FTP_HOST = data["FTP_HOST"]
    FTP_USER = data["FTP_USER"]
    FTP_PASS = data["FTP_PASS"]

logging.info("getting files from ftp")
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
files = ftp.nlst()

#starting time
time_now = time.time()

#download file
def download_file(ftp_client, file_path):
    ftp_client = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    with open(file_path, 'wb') as f:
        ftp_client.retrbinary(f'RETR {file_path}', f.write)
        logging.info(f"{f} is written")

#download asynchronously
def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_file, ftp, file) for file in files]
        for future in futures:
            future.result()
    logging.info(f"Time taken: {time.time() - time_now} seconds")
    os.startfile(".")

main()