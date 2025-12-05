# 🏠 IdealiScrape

**IdealiScrape** is a real estate tool that monitors [Idealista](https://www.idealista.com) for new listings using the **Official Idealista API**. It sends instant notifications to your Telegram channel when new properties matching your criteria are found.

## ✨ Features

- **🚀 Official API Integration**: Fast, reliable, and no more CAPTCHAs or blocks!
- **🔍 Parametric Search**: Filter by location (coordinates or zone name), price, type (Sale/Rent), and distance.
- **📱 Telegram Notifications**: Instant formatted alerts with Price, Size, Location, and Link.
- **💾 Database Storage**: Prevents duplicate notifications by tracking listings in a local SQLite database (`data/listings.db`).

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Idealista API Keys (Request at [developers.idealista.com](https://developers.idealista.com))

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
    Create a `.env` file in the root directory:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` with your credentials:
    ```env
    TELEGRAM_TOKEN=your_bot_token
    TELEGRAM_CHAT_ID=your_chat_id
    IDEALISTA_API_KEY=your_api_key
    IDEALISTA_API_SECRET=your_api_secret
    ```

## 🛠 Usage

Run the tool using `main.py`.

### Basic Command (Madrid Sol default)
```bash
python main.py --type rent --price-max 1200
```

### Options

| Argument | Description | Default | Example |
| :--- | :--- | :--- | :--- |
| `--center` | Coordinates (Lat,Lng) | `40.4167,-3.70325` (Madrid) | `--center "41.3851,2.1734"` |
| `--zone` | Name of zone/city to search via Nominatim | `None` | `--zone "Valencia"` |
| `--distance` | Search radius in meters | `3000` | `--distance 5000` |
| `--price-max` | Maximum price filter | `None` | `--price-max 1500` |
| `--type` | Listing type: `sale` or `rent` | `sale` | `--type rent` |

### Examples

**Rentals in Barcelona (Center) under 1500€:**
```bash
python main.py --type rent --price-max 1500 --center "41.3851,2.1734"
```

**Rentals in Valencia (Zone Name):**
```bash
python main.py --type rent --zone "Valencia"
```

**Sales in Madrid within 1km of Sol:**
```bash
python main.py --type sale --distance 1000
```

## 📂 Project Structure

```
IdealiScrape/
├── data/
│   └── listings.db       # SQLite database
├── src/
│   ├── api.py            # Official API Client (Auth, Search)
│   ├── database.py       # Database operations
│   ├── notifier.py       # Telegram notification logic
│   └── settings.py       # Configuration loader
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── .env                  # Secrets
```

## ⚠️ Disclaimer
This tool is for educational purposes. Ensure you comply with Idealista's API Terms of Service.
