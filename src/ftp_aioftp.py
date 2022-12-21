import asyncio
import aioftp
import time, json
import ftplib
time_now = time.time()
with open("./data/config.json") as file:
    data = json.load(file)
    FTP_HOST = data["FTP_HOST"]
    FTP_USER = data["FTP_USER"]
    FTP_PASS = data["FTP_PASS"]


async def download_file(path):
    async with aioftp.Client.context(FTP_HOST, user=FTP_USER, password=FTP_PASS) as client:
        await client.download(path)

async def main():
    #getting files from ftp server
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    files = ftp.nlst()
    #start downloading
    tasks = [download_file(path) for path in files]
    await asyncio.gather(*tasks)

asyncio.run(main())
print((f"Time taken: {time.time() - time_now} seconds"))