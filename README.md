# 🏠 IdealiScrape

**IdealiScrape** is a powerful and customizable Python scraper for real estate listings on [Idealista](https://www.idealista.com). It monitors new listings matching your criteria and sends instant notifications to your Telegram channel.

It is designed to bypass basic anti-scraping measures using `undetected-chromedriver` and mimics human behavior.

## ✨ Features

- **🔍 Parametric Search**: Filter by zone, neighborhood, price, and listing type (Sale/Rent).
- **📱 Telegram Notifications**: Get instant alerts with details (Price, Size, Location, Link) directly to your phone.
- **💾 Database Storage**: Stores findings in a local SQLite database (`data/listings.db`) to prevent duplicate notifications.
- **👻 Stealth Mode**: Runs in **Headless Mode** by default (invisible browser) with anti-detection headers.
- **🐛 Debugging**: Includes a visible browser mode (`--no-headless`) and automatic screenshot capture on errors.

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Google Chrome browser installed.

### Steps
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/IdealiScrape.git
    cd IdealiScrape
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**:
    Create a `.env` file in the root directory (copy from `.env.example`):
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and add your Telegram credentials:
    ```env
    TELEGRAM_TOKEN=your_bot_token
    TELEGRAM_CHAT_ID=your_chat_id
    ```

## 🛠 Usage

Run the scraper using `main.py`. By default, it runs in **headless mode** (invisible).

### Basic Command
```bash
python main.py
```

### Filters & Arguments

| Argument | Description | Default | Example |
| :--- | :--- | :--- | :--- |
| `--zone` | City or Zone to search | `madrid` | `--zone barcelona` |
| `--neighborhood` | Specific neighborhood | `ciudad-lineal` | `--neighborhood gracia` |
| `--price-max` | Maximum price filter | `1200` | `--price-max 1500` |
| `--type` | Listing type: `sale` or `rent` | `rent` | `--type sale` |
| `--no-headless` | Run with visible browser window | `False` | `--no-headless` |

### Examples

**Search for Rentals in Madrid (Ciudad Lineal) under 1200€:**
```bash
python main.py --type rent --zone madrid --neighborhood ciudad-lineal --price-max 1200
```

**Search for Sales in Barcelona under 500k€:**
```bash
python main.py --type sale --zone barcelona --price-max 500000
```

**Debug Mode (Visible Browser):**
```bash
python main.py --no-headless
```

## 📂 Project Structure

```
IdealiScrape/
├── data/
│   └── listings.db       # SQLite database (auto-created)
├── src/
│   ├── scraper.py        # Logic for Selenium & BeautifulSoup
│   ├── database.py       # Database operations
│   ├── notifier.py       # Telegram notification logic
│   └── settings.py       # Configuration loader
├── main.py               # Entry point
├── requirements.txt      # Python dependencies
└── .env                  # Secrets (gitignored)
```

## ⚠️ Disclaimer
This tool is for educational purposes only. Scraping websites without permission may violate their Terms of Service. Use responsibly and respect rate limits.
