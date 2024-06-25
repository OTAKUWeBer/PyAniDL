# Anime Episode Downloader

Anime Episode Downloader is a Python script that facilitates searching for anime on Anitaku and downloading episodes from Gogoanime using asynchronous requests.

## Features

- **Search Anime**: Enter the name of the anime you're looking for on Anitaku and browse results.
- **Download Episodes**: Select an anime from the search results and download episodes from Gogoanime in various qualities.
- **Asynchronous Requests**: Utilizes `asyncio` and `aiohttp` for non-blocking HTTP requests, enhancing performance when fetching and downloading episodes asynchronously.
- **HTML Parsing**: Uses `BeautifulSoup` for parsing HTML content from web pages to extract anime details and episode download links.
- **External Commands Execution**: Utilizes `subprocess` for executing external commands if required.
- **HTTP Requests**: Utilizes `requests` for making synchronous HTTP requests when necessary.
- **Interactive Selection**: Provides a smooth selection interface using `questionary` for browsing and selecting anime from search results.
- **Cross-Platform Compatibility**: Supports Windows, macOS, and Linux operating systems for seamless execution.
- **Download Directory Management**: Automatically creates a directory for downloaded anime episodes if it doesn't exist.
- **Resume Capability:** Supports resuming interrupted downloads by utilizing HTTP Range requests.
- **Download Progress:** Displays a progress bar during downloads using `tqdm` for improved user experience.

## Prerequisites

- Python 3.7 or higher installed on your system.
- Required Python packages (`aiohttp`, `beautifulsoup4`, `requests`, `validators`, `questionary`, `nest_asyncio`, `tqdm`, `termcolor`), which can be installed via `pip`.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/OTAKUWeBer/PyAniDL.git
   cd PyAniDL
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure cookies:**

   Update the necessary cookies in the script (`main.py`) for authentication with Gogoanime.

## Usage

1. **Run the script:**

   ```bash
   python main.py
   ```

2. **Follow the prompts:**

   - Choose "1" to find an anime on Anitaku and follow the prompts to select an anime and view details.
   - Choose "2" to directly download episodes by providing a Gogoanime link.

3. **Download episodes:**

   - Specify the range and quality of episodes to download when prompted.

## Configuration

- Ensure your `cookies` in `main.py` are correctly set for authentication with Gogoanime.

## External Commands

- The script may use `subprocess` for executing external commands if required for specific functionality.

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/awesome-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add awesome feature'`).
5. Push to the branch (`git push origin feature/awesome-feature`).
6. Create a new Pull Request.
