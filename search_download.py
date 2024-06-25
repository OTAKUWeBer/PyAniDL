import asyncio
import aiohttp
import os
import subprocess
import questionary
import nest_asyncio
from bs4 import BeautifulSoup
from tqdm import tqdm
from termcolor import colored
from id_grab import grab_id

# Apply the nest_asyncio patch
nest_asyncio.apply()

# Define COOKIES
COOKIES = {
    '_ga_X2C65NWLE2': 'GS1.1.1718531678.3.0.1718531678.0.0.0',
    '_ga': 'GA1.1.251359287.1718516408',
    'gogoanime': '2stn8gti5vihjk80dnhgvh3s72',
    'auth': 'KhXMsD6IEey4qis2s%2F0Z4mnIjleMwfcORDZuXzqiXnhuF5Dnuq6iqNS4OrJ%2Bz1uqm1MJt%2BcgHZ0GKakQT1CapQ%3D%3D',
}

def clear_screen():
    """Clear the console screen."""
    if os.name == 'nt':  # For Windows
        subprocess.run(['cls'], shell=True)
    else:  # For Unix/Linux/Mac
        subprocess.run(['clear'])

clear_screen()

async def search_anime():
    """Search for an anime and display the results."""
    while True:
        results = {}
        
        try:
            search = questionary.text("Enter anime name to search or 'q' to quit: ", style=questionary.Style([('answer', 'fg:green')])).ask()
            if search.lower() == 'q':
                clear_screen()
                print(colored("Exiting anime search.", 'red'))
                return
        except KeyboardInterrupt:
            print(colored("\nSearch interrupted. Exiting.", 'red'))
            return
        
        url = f"https://anitaku.pe/search.html?keyword={search}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()

        soup = BeautifulSoup(html, "html.parser")
        anime_list = soup.find_all("ul", {"class": "items"})

        for ul in anime_list:
            items = ul.find_all("li")
            for item in items:
                title = item.find("a").get("title")
                link = item.find("a").get("href")
                results[title] = f"https://anitaku.pe{link}"
        
        if not results:
            clear_screen()
            print(colored("No results found. Please try searching again.", 'red'))
            continue

        choices = list(results.keys())
        selected_choice = questionary.select(
            "Select anime to see details, or 'q' to quit:",
            choices=choices + ["--quit"],
            style=questionary.Style([
                ('selected', 'fg:yellow'),
                ('pointer', 'fg:yellow'),
                ('highlighted', 'fg:yellow'),
                ('selected', 'bg:yellow fg:black'),
            ])
        ).ask()

        if selected_choice == 'q' or selected_choice == "--quit":
            clear_screen()
            print(colored("Exiting anime search.", 'red'))
            return

        selected_title = selected_choice
        selected_link = results[selected_title]
        await display_anime_details(selected_title, selected_link)

async def display_anime_details(title, selected_link):
    """Display details of the selected anime."""
    async with aiohttp.ClientSession() as session:
        async with session.get(selected_link) as detail_response:
            detail_html = await detail_response.text()

    detail_soup = BeautifulSoup(detail_html, "html.parser")
    anime_info_body = detail_soup.find("div", {"class": "anime_info_body"})
    
    if anime_info_body:
        image_url = anime_info_body.find("img")["src"]
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
            total_episodes = colored("Unknown", 'red')
        print(f"\033[1mTotal Episodes:\033[0m {total_episodes}\n")
        
        download_choice = questionary.confirm("Download episodes from this?").ask()
        if download_choice:
            await fetch_episode_links(selected_link, title)
        else:
            clear_screen()
            print(colored("Download cancelled.", 'red'))

async def fetch_episode_links(selected_link, title):
    """Fetch episode links for the selected anime and download them."""
    code = grab_id(selected_link)
    start = questionary.text("Download episode from (number): ").ask()
    end = questionary.text("To: ").ask()
    QUALITY = "1280x720"
    anime_eps_url = f"https://ajax.gogocdn.net/ajax/load-list-episode?ep_start={start}&ep_end={end}&id={code}"

    download_directory = os.path.join(os.getcwd(), "downloaded_animes", title)
    os.makedirs(download_directory, exist_ok=True)

    download_links = []
    async with aiohttp.ClientSession() as session:
        async with session.get(anime_eps_url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                container = soup.find("ul", {"id": "episode_related"})
                if container:
                    for list_item in container.find_all("li"):
                        link = list_item.find("a")
                        if link:
                            episode_link = f"https://anitaku.pe{link['href'][1:]}"
                            download_links.append(episode_link)
                else:
                    clear_screen()
                    print(colored('No episodes found on the page.', 'red'))
            else:
                print(colored(f"Failed to retrieve episode list, status code: {response.status}", 'red'))

    semaphore = asyncio.Semaphore(2)  # Limit to 2 concurrent downloads
    tasks = [download_file(url, COOKIES, QUALITY, os.path.join(download_directory, f"{url.split('/')[-1]}.mp4"), semaphore) for url in reversed(download_links)]
    await asyncio.gather(*tasks)

async def download_file(url, COOKIES, res, local_filename, semaphore, chunk_size=1024, fallback_res=['1920x1080', '854x480', '640x360']):
    """Download an episode file with the specified resolution."""
    async with semaphore:
        async with aiohttp.ClientSession(cookies=COOKIES) as session:
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

async def search():
    """Initiate the anime search."""
    await search_anime()

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(search())