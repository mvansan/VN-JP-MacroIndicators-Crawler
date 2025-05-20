import subprocess
import sys

def run_cpi_crawlers():
    print("Starting CPI data collection process...")
    
    print("\nRunning Vietnam CPI crawler...")
    vn_result = subprocess.run([sys.executable, "crawler/vn_cpi_crawler.py"])
    
    print("\nRunning Japan CPI crawler...")
    jp_result = subprocess.run([sys.executable, "crawler/jp_cpi_crawler.py"])
    
    if vn_result.returncode == 0 or jp_result.returncode == 0:
        print("\nNew data found in at least one crawler. Running data processing...")
        
        print("\nRunning CPI data cleaner...")
        subprocess.run([sys.executable, "cleaner/cpi_cleaner.py"])
        
        print("\nRunning CPI data visualizer...")
        subprocess.run([sys.executable, "visualize/cpi_visualizer.py"])
        
        print("\nCPI data collection and processing completed successfully!")
    else:
        print("\nNo new data found in either crawler. Process stopped.")

if __name__ == "__main__":
    run_cpi_crawlers() 