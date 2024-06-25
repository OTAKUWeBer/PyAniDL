<h1 align="center">
    <img align="center" height="80px" width="80px" src="https://raw.githubusercontent.com/OTAKUWeBer/PyAniDL/main/assets/icon.png" alt="PyAniDL">PyAniDL
</h1>

*PyAniDL* is a powerful tool for downloading anime from Gogoanime built on Python. It offers a range of features to ensure a smooth and efficient download experience.

<img align="center" src="https://raw.githubusercontent.com/OTAKUWeBer/PyAniDL/main/assets/ss1.jpg" alt="screenshot-1">
<img align="center" src="https://raw.githubusercontent.com/OTAKUWeBer/PyAniDL/main/assets/ss2.jpg" alt="screanshot-2">

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
- **Resume Capability**: Supports resuming interrupted downloads by utilizing HTTP Range requests.
- **Download Progress**: Displays a progress bar during downloads using `tqdm` for improved user experience.
- **Video Quality Selection**: Automatically selects the best available video quality (1080p, 480p, 360p) if the preferred quality (720p) is not available.

## Prerequisites

- Python 3.7 or higher installed on your system.
- Required Python packages (`aiohttp`, `beautifulsoup4`, `requests`, `validators`, `questionary`, `nest_asyncio`, `tqdm`, `termcolor`), which can be installed via pip.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/OTAKUWeBer/PyAniDL.git
    cd PyAniDL
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the script:**

   ```sh
   python main.py
   ```

2. **Follow the prompts:**

   - Choose "1" to find an anime on Anitaku and follow the prompts to select an anime and view details.
   - Choose "2" to directly download episodes by providing a Gogoanime link.

3. **Download episodes:**

   - Specify the range and quality of episodes to download when prompted.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.
