import subprocess
import sys

def run_bond_yield_crawlers():
    print("Starting Bond Yield data collection process...")
    
    print("\nRunning Vietnam Bond Yield crawler...")
    vn_result = subprocess.run([sys.executable, "crawler/vn_bond_yield_crawler.py"])
    
    print("\nRunning Japan Bond Yield crawler...")
    jp_result = subprocess.run([sys.executable, "crawler/jp_bond_yield_crawler.py"])
    
    if vn_result.returncode == 0 or jp_result.returncode == 0:
        print("\nNew data found in at least one crawler. Running data processing...")
        
        print("\nRunning Bond Yield data cleaners...")
        subprocess.run([sys.executable, "cleaner/vn_bond_yield_cleaner.py"])
        subprocess.run([sys.executable, "cleaner/jp_bond_yield_cleaner.py"])
        
        print("\nRunning Bond Yield data visualizers...")
        subprocess.run([sys.executable, "visualize/vn_bond_yield_visualizer.py"])
        subprocess.run([sys.executable, "visualize/jp_bond_yield_visualizer.py"])
        
        print("\nBond Yield data collection and processing completed successfully!")
    else:
        print("\nNo new data found in either crawler. Process stopped.")

if __name__ == "__main__":
    run_bond_yield_crawlers() 