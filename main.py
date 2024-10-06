import asyncio
from anime_downloader import link
from anime_downloader import search
import subprocess
import os

def clear_screen():
    if os.name == 'nt':  # For Windows
        subprocess.run(['cls'], shell=True)
    else:  # For Unix/Linux/Mac
        subprocess.run(['clear'])

async def download_episode():
    while True:
        print("How would you like to download the episode?")
        print("1. Search for episode")
        print("2. Direct download link")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            clear_screen()
            await search()
        elif choice == "2":
            clear_screen()
            await link()
        else:
            print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    asyncio.run(download_episode())