# VN-JP MacroIndicators Crawler

## Features
- **Vietnam & Japan Bond Yield Crawler**: Scrapes 5-year government bond yield data from Investing.com for both Vietnam and Japan.
- **Vietnam Interbank Interest Rate Crawler**: Extracts daily interbank interest rates from the State Bank of Vietnam.
- **Japan CPI Crawler**: Collects monthly Consumer Price Index (CPI) data from Japan's e-Stat portal.
- **Vietnam CPI Crawler**: Gathers monthly CPI data from Vietstock.
- **Data Cleaning Scripts**: Standardize, fill missing values, and preprocess all macro datasets for analysis.
- **Visualization Scripts**: Generate insightful plots and comparisons for all macro indicators, including cross-country bond yield comparison.
- **Automated Cloud Storage**: After crawling and cleaning, new data is automatically uploaded to AWS S3 (cloud) via GitHub Actions, ensuring only new data is stored.

## Folder Structure
```
├── .github/workflows/         # GitHub Actions workflows for automation
├── crawler/                   # All web crawlers for raw data
├── cleaner/                   # Data cleaning scripts
├── store_data/                # Scripts to upload cleaned data to AWS S3
├── data/
│   ├── raw/                   # Raw data after crawling
│   └── cleaned/               # Cleaned and standardized data
├── visualize/                 # Visualization scripts and output images
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
```

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
  - python-dotenv
  - boto3

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

### 1.1. Run the full Bond Yield pipeline (crawl, clean, visualize)
To automate the entire process for both Vietnam and Japan bond yields, use:
```bash
python crawler/run_bond_yield_crawlers.py
```
This script will:
- Run both Vietnam and Japan bond yield crawlers
- Clean the data
- Generate all related visualizations
- Only process and visualize if new data is found

### 1.2. Run the full CPI pipeline (crawl, clean, visualize)
To automate the entire process for both Vietnam and Japan CPI, use:
```bash
python crawler/run_cpi_crawlers.py
```
This script will:
- Run both Vietnam and Japan CPI crawlers
- Clean the data
- Generate all related visualizations
- Only process and visualize if new data is found

### 2. Clean and standardize data
Run the cleaning scripts from the `cleaner/` directory to produce cleaned datasets in `data/cleaned/`:
```bash
python cleaner/vn_bond_yield_cleaner.py
python cleaner/jp_bond_yield_cleaner.py
python cleaner/cpi_cleaner.py
python cleaner/vn_interbank_cleaner.py
```

### 3. Store data to AWS S3 (Cloud)
- **Automatically via GitHub Actions:**
  - After each successful crawl and commit, GitHub Actions will run the corresponding `store_data/*.py` script to upload only new data to AWS S3.
  - AWS credentials are managed via GitHub repository secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`).
- **Manually (optional):**
  - You can run any script in `store_data/` locally to upload cleaned data to S3 (requires `.env` or environment variables for AWS credentials).

### 4. Visualize and analyze
Run the visualization scripts from the `visualize/` directory to generate plots in `visualize/images/`:
```bash
python visualize/vn_bond_yield_visualizer.py
python visualize/jp_bond_yield_visualizer.py
python visualize/bond_yield_comparison_visualizer.py
python visualize/cpi_visualizer.py
python visualize/vn_interbank_interest_visualizer.py
```

## Automation with GitHub Actions
- Workflows are defined in `.github/workflows/` for each data type.
- Each workflow will:
  1. Crawl new data
  2. Commit changes if new data is found
  3. Store only new data to AWS S3 using the corresponding script in `store_data/`
- **No duplicate uploads:** The store scripts check the latest data on S3 and only upload new entries.

## Notes
- Ensure you have a stable internet connection and Google Chrome installed.
- Crawlers use Selenium WebDriver and may take several minutes to complete depending on the data range.
- For best results, use the latest version of Chrome and ChromeDriver.
- Sometimes, the Investing.com website may fail to load or respond. If this happens, please close the browser window and rerun the script.
- Visualization scripts will output PNG files to `visualize/images/` for further analysis and reporting.
- For cloud upload, make sure your AWS credentials are set up as GitHub secrets or in your local environment if running manually.

## License
This project is for research and educational purposes only.
