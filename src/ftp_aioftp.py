import asyncio
import aioftp
import time
import ftplib
time_now = time.time()

async def download_file(path):
    async with aioftp.Client.context("ftp3.interactivebrokers.com", user="shortstock", password="") as client:
        await client.download(path)

async def main():
    ftp = ftplib.FTP("ftp3.interactivebrokers.com", "shortstock", "")
    files = ftp.nlst()
    async with aioftp.Client.context("ftp3.interactivebrokers.com", user="shortstock", password="") as client:
        tasks = [download_file(path) for path in files]
        await asyncio.gather(*tasks)

asyncio.run(main())
print((f"Time taken: {time.time() - time_now} seconds"))