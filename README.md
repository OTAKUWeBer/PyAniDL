<h1 align="center">
    <img align="center" height="80px" width="80px" src="https://raw.githubusercontent.com/OTAKUWeBer/PyAniDL/main/assets/icon.png" alt="PyAniDL">PyAniDL
</h1>

*PyAniDL* is a powerful tool for downloading anime from Gogoanime built on Python. It offers a range of features to ensure a smooth and efficient download experience.

<img align="center" src="https://raw.githubusercontent.com/OTAKUWeBer/PyAniDL/main/assets/ss1.jpg" alt="screenshot-1">
<img align="center" src="https://raw.githubusercontent.com/OTAKUWeBer/PyAniDL/main/assets/ss2.jpg" alt="screanshot-2">

## Features

- **Search Anime**: Enter the name of the anime you're looking for on Anitaku and browse results.
- **Download Directory Management**: Automatically creates a directory for downloaded anime episodes if it doesn't exist.
- **Concurrent Downloads**: Download multiple episodes simultaneously to save time.
- **Complete Season or Episode Range**: Download a full season or select specific episodes (e.g., episodes 1-12).
- **Resume Capability**: Supports resuming interrupted downloads by utilizing HTTP Range requests.
- **Download Progress**: Displays a progress bar during downloads using `tqdm` for improved user experience.
- **Video Quality Selection**: Automatically selects the best available video quality (1080p) if the preferred quality (720p) is not available.

## Prerequisites

- Python 3.7 or higher installed on your system.
- Required Python packages (`aiohttp`, `beautifulsoup4`, `questionary`, `nest_asyncio`, `tqdm`, `termcolor`) which can be installed via pip.

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