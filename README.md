## Features
- **Vietnam & Japan Bond Yield Crawler**: Scrapes 5-year government bond yield data from Investing.com for both Vietnam and Japan.
- **Vietnam Interbank Interest Rate Crawler**: Extracts daily interbank interest rates from the State Bank of Vietnam.
- **Japan CPI Crawler**: Collects monthly Consumer Price Index (CPI) data from Japan's e-Stat portal.
- **Vietnam CPI Crawler**: Gathers monthly CPI data from Vietstock.
- **Data Cleaning Scripts**: Standardize, fill missing values, and preprocess all macro datasets for analysis.
- **Visualization Scripts**: Generate insightful plots and comparisons for all macro indicators, including cross-country bond yield comparison.

## Output
All data is saved as CSV files in the `data/` directory:
- `data/raw/` — Raw data after crawling
  - `vn_bond_yield.csv` — Vietnam 5-year bond yields
  - `jp_bond_yield.csv` — Japan 5-year bond yields
  - `vn_interbank_interest.csv` — Vietnam interbank interest rates
  - `jp_cpi.csv` — Japan monthly CPI
  - `vn_cpi.csv` — Vietnam monthly CPI
- `data/cleaned/` — Cleaned and standardized data
  - `vn_bond_yield_cleaned.csv`
  - `jp_bond_yield_cleaned.csv`
  - `cpi_data.csv`
  - `vn_interbank_interest_clean.csv`

## Requirements
- Python 3.x
- Google Chrome browser
- ChromeDriver (automatically managed by `webdriver-manager`)
- The following Python packages:
  - selenium
  - webdriver-manager
  - pandas
  - matplotlib
  - seaborn

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/mvansan/VN-JP-MacroIndicators-Crawler.git
   cd VN-JP-MacroIndicators-Crawler
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### 1. Crawl raw data
Run the desired crawler script from the `crawler/` directory. For example:
```bash
python crawler/vn_jp_bond_yield_crawler.py
python crawler/vn_interbank_interest_crawler.py
python crawler/jp_cpi_crawler.py
python crawler/vn_cpi_crawler.py
```
Raw CSV files will be saved in `data/raw/`.

### 2. Clean and standardize data
Run the cleaning scripts from the `cleaner/` directory to produce cleaned datasets in `data/cleaned/`:
```bash
python cleaner/vn_bond_yield_cleaner.py
python cleaner/jp_bond_yield_cleaner.py
python cleaner/cpi_cleaner.py
python cleaner/vn_interbank_cleaner.py
```

### 3. Visualize and analyze
Run the visualization scripts from the `visualize/` directory to generate plots in `visualize/images/`:
```bash
python visualize/vn_bond_yield_visualizer.py
python visualize/jp_bond_yield_visualizer.py
python visualize/bond_yield_comparison_visualizer.py
python visualize/cpi_visualizer.py
python visualize/vn_interbank_interest_visualizer.py
```

## Notes
- Ensure you have a stable internet connection and Google Chrome installed.
- Crawlers use Selenium WebDriver and may take several minutes to complete depending on the data range.
- For best results, use the latest version of Chrome and ChromeDriver.
- Sometimes, the Investing.com website may fail to load or respond. If this happens, please close the browser window and rerun the script.
- Visualization scripts will output PNG files to `visualize/images/` for further analysis and reporting.

## License
This project is for research and educational purposes only.
