import asyncio
import aiohttp
import os
import subprocess
import questionary
from bs4 import BeautifulSoup
from tqdm import tqdm
import nest_asyncio
from termcolor import colored
import validators
from id_grab import grab_id

# Apply the nest_asyncio patch
nest_asyncio.apply()

# Constants
COOKIES = {
    '_ga_X2C65NWLE2': 'GS1.1.1718531678.3.0.1718531678.0.0.0',
    '_ga': 'GA1.1.251359287.1718516408',
    'gogoanime': '2stn8gti5vihjk80dnhgvh3s72',
    'auth': 'KhXMsD6IEey4qis2s%2F0Z4mnIjleMwfcORDZuXzqiXnhuF5Dnuq6iqNS4OrJ%2Bz1uqm1MJt%2BcgHZ0GKakQT1CapQ%3D%3D',
}
QUALITY = "1280x720"
DOWNLOAD_DIRECTORY = os.path.join(os.getcwd(), "downloaded_animes")

gogo_url = "https://anitaku.pe"


# List of fallback resolutions
fallback_res = [
    "1280x720",
    "960x720",
    "1920x1080",
    "1440x1080",
    "854x480",
    "720x576",
    "720x480",
    "640x480",
    "640x360",
    "480x360",
    "638x360"
]

# Ensure the download directory exists
os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)

# Function to clear the screen
def clear_screen():
    if os.name == 'nt':  # For Windows
        subprocess.run(['cls'], shell=True)
    else:  # For Unix/Linux/Mac
        subprocess.run(['clear'])

clear_screen()

async def get_episodes_links(anime_eps_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(anime_eps_url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                container = soup.find("ul", {"id": "episode_related"})
                if container:
                    links = [f"{gogo_url}{li.find('a')['href'][1:]}" for li in container.find_all("li")]
                    return links
                else:
                    print(colored(f"Failed to retrieve episode list, status code: {response.status}", 'red'))
            else:
                print(colored(f"Failed to retrieve page, status code: {response.status}", 'red'))
            return []

async def download_file(url, cookies, res, local_filename, semaphore, fallback_res=fallback_res, chunk_size=1024):
    """Download an episode file with the specified resolution."""
    async with semaphore:
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    container = soup.find("div", {"class": "cf-download"})
                    if container:
                        links = container.find_all("a")
                        download_link = next((link['href'] for link in links if res in link.text), None)
                        
                        if not download_link:
                            # Try fallback resolutions
                            for fallback in fallback_res:
                                download_link = next((link['href'] for link in links if fallback in link.text), None)
                                if download_link:
                                    break
                        
                        if download_link:
                            headers = {}
                            # Check if the file already exists to resume download
                            if os.path.exists(local_filename):
                                downloaded_size = os.path.getsize(local_filename)
                                headers['Range'] = f'bytes={downloaded_size}-'
                            else:
                                downloaded_size = 0

                            async with session.get(download_link, headers=headers, timeout=None) as download_response:
                                total_size = int(download_response.headers.get('content-length', 0)) + downloaded_size
                                display_name = os.path.basename(local_filename)
                                
                                # Ensure the directory exists before downloading
                                os.makedirs(os.path.dirname(local_filename), exist_ok=True)
                                
                                with open(local_filename, 'ab') as file:
                                    with tqdm(total=total_size, unit='iB', unit_scale=True, desc=display_name, initial=downloaded_size) as t:
                                        while True:
                                            chunk = await download_response.content.read(chunk_size)
                                            if not chunk:
                                                break
                                            file.write(chunk)
                                            t.update(len(chunk))
                            print("☑", end="")
                            print(colored(f" File downloaded successfully and saved as {local_filename}", 'green'))
                        else:
                            print(colored("Requested quality not available and no fallback found.", 'red'))
                    else:
                        print(colored('Download link container not found.', 'red'))
                else:
                    print(colored(f"Failed to retrieve download link, status code: {response.status}", 'red'))

def get_valid_url(prompt_text):
    while True:
        url = questionary.text(prompt_text).ask()
        if validators.url(url):
            return url
        else:
            print(colored("Invalid input. Please enter a valid URL.", 'red'))

async def display_anime_details(selected_link):
    """Display details of the selected anime."""
    async with aiohttp.ClientSession() as session:
        async with session.get(selected_link) as detail_response:
            detail_html = await detail_response.text()

    detail_soup = BeautifulSoup(detail_html, "html.parser")
    anime_info_body = detail_soup.find("div", {"class": "anime_info_body"})
    
    if anime_info_body:
        image_url = anime_info_body.find("img")["src"]
        title = anime_info_body.find("h1").text.strip()
        anime_info = {"title": title, "image_url": image_url}

        for p in anime_info_body.find_all("p", {"class": "type"}):
            span_tag = p.find("span")
            if span_tag:
                key = span_tag.text.lower().strip().replace(" ", "_").replace(":", "")
                span_tag.extract()
                value = p.text.strip()
                anime_info[key] = value

        description_div = anime_info_body.find("div", {"class": "description"})
        if description_div:
            anime_info["plot_summary"] = description_div.text.strip()
        
        print(f"\033[1mTitle:\033[0m {anime_info.get('title')}")
        print(f"\033[1mThumbnail:\033[0m {anime_info.get('image_url')}")
        print("\033[1mAbout:\033[0m")
        
        plot_summary = anime_info.get('plot_summary')
        if plot_summary:
            plot_summary = plot_summary.split('Genres:')[0].strip()
        print(f"  \033[1mPlot summary:\033[0m {plot_summary}\n")
        print(f"  \033[1mType:\033[0m {anime_info.get('type')}")
        print(f"  \033[1mGenre:\033[0m {anime_info.get('genre')}")
        print(f"  \033[1mReleased:\033[0m {anime_info.get('released')}")
        print(f"  \033[1mStatus:\033[0m {anime_info.get('status')}\n")
        
        episode_page = detail_soup.find("ul", {"id": "episode_page"})
        if episode_page:
            last_episode = episode_page.find_all("li")[-1]
            total_episodes = last_episode.find("a")["ep_end"]
        else:
            total_episodes = "Unknown"
        print(f"\033[1mTotal Episodes:\033[0m {total_episodes}\n")
        
        download_choice = questionary.confirm("Download episodes from this?").ask()
        if download_choice:
            start = questionary.text("Download episode from (number): ").ask()
            end = questionary.text("To: ").ask()
            anime_eps_url = f"https://ajax.gogocdn.net/ajax/load-list-episode?ep_start={start}&ep_end={end}&id={grab_id(selected_link)}"
            await fetch_episode_links(anime_eps_url, anime_info.get('title'))
        else:
            clear_screen()
            print(colored("Download cancelled.", 'red'))

async def fetch_episode_links(anime_eps_url, title):
    episode_links = await get_episodes_links(anime_eps_url)
    if not episode_links:
        return

    semaphore = asyncio.Semaphore(2)  # Limit to 2 concurrent downloads
    tasks = [
        download_file(
            url,
            COOKIES,
            QUALITY,
            os.path.join(DOWNLOAD_DIRECTORY, title, f"{url.split('/')[-1]}.mp4"),
            semaphore
        )
        for url in reversed(episode_links)
    ]
    await asyncio.gather(*tasks)

async def link():
    link = get_valid_url("Drop the anime link from GoGoanime (anitaku): ")
    await display_anime_details(link)

if __name__ == "__main__":
    asyncio.run(link())