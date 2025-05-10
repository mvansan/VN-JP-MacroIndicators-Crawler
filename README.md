## Features
- **Vietnam & Japan Bond Yield Crawler**: Scrapes 5-year government bond yield data from Investing.com for both Vietnam and Japan.
- **Vietnam Interbank Interest Rate Crawler**: Extracts daily interbank interest rates from the State Bank of Vietnam.
- **Japan CPI Crawler**: Collects monthly Consumer Price Index (CPI) data from Japan's e-Stat portal.
- **Vietnam CPI Crawler**: Gathers monthly CPI data from Vietstock.

## Output
All crawled data is saved as CSV files in the `data/` directory:
- `data/vn_bond_yield.csv` — Vietnam 5-year bond yields
- `data/jp_bond_yield.csv` — Japan 5-year bond yields
- `data/vn_interbank_interest.csv` — Vietnam interbank interest rates
- `data/jp_cpi.csv` — Japan monthly CPI
- `data/vn_cpi.csv` — Vietnam monthly CPI

## Requirements
- Python 3.x
- Google Chrome browser
- ChromeDriver (automatically managed by `webdriver-manager`)
- The following Python packages:
  - selenium
  - webdriver-manager
  - pandas (for interbank interest rate crawler)

## Installation
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd VN-JP-MacroIndicators-Crawler
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the desired crawler script from the `crawler/` directory. For example:

```bash
python crawler/vn_jp_bond_yield_crawler.py
python crawler/vn_interbank_interest_crawler.py
python crawler/jp_cpi_crawler.py
python crawler/vn_cpi_crawler.py
```

The output CSV files will be saved in the `data/` directory.

## Notes
- Ensure you have a stable internet connection and Google Chrome installed.
- Crawlers use Selenium WebDriver and may take several minutes to complete depending on the data range.
- For best results, use the latest version of Chrome and ChromeDriver.

## License
This project is for research and educational purposes only.
