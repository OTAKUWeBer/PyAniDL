from bs4 import BeautifulSoup
import aiohttp

async def grab_id(url):
    """Grab the anime ID from the anime details page asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_content = await response.text()
            soup = BeautifulSoup(response_content, "html.parser")
            anime_id = soup.find("input", {"id": "movie_id"})["value"]
            
            return anime_id