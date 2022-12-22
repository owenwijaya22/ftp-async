import asyncio, aioftp
import time, json, logging, sys
import ftplib

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

time_now = time.time()
with open("./data/config.json") as file:
    data = json.load(file)
    FTP_HOST = data["FTP_HOST"]
    FTP_USER = data["FTP_USER"]
    FTP_PASS = data["FTP_PASS"]


async def download_file(file):
    async with aioftp.Client.context(FTP_HOST, user=FTP_USER, password=FTP_PASS) as client:
        await client.download(file)
        logger.info(f"{file} is written")

async def main():
    #getting files from ftp server
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    files = ftp.nlst()
    #start downloading
    tasks = [download_file(file) for file in files]
    await asyncio.gather(*tasks)

asyncio.run(main())
logger.info(f"Time taken: {time.time() - time_now} seconds")