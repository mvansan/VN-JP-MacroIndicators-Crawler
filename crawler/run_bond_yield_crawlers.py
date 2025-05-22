import subprocess
import sys

def run_with_retry(cmd, name, max_retries=2):
    for attempt in range(1, max_retries + 1):
        print(f"\nRunning {name} (attempt {attempt})...")
        result = subprocess.run(cmd)
        if result.returncode == 0:
            return result
        print(f"{name} failed (attempt {attempt}).")
    print(f"{name} failed after {max_retries} attempts.")
    return result

def run_bond_yield_crawlers():
    print("Starting Bond Yield data collection process...")
    
    vn_result = run_with_retry([sys.executable, "crawler/vn_bond_yield_crawler.py"], "Vietnam Bond Yield crawler")
    jp_result = run_with_retry([sys.executable, "crawler/jp_bond_yield_crawler.py"], "Japan Bond Yield crawler")
    
    if vn_result.returncode == 0 or jp_result.returncode == 0:
        print("\nNew data found in at least one crawler. Running data processing...")
        
        print("\nRunning Bond Yield data cleaners...")
        subprocess.run([sys.executable, "cleaner/vn_bond_yield_cleaner.py"])
        subprocess.run([sys.executable, "cleaner/jp_bond_yield_cleaner.py"])
        
        print("\nRunning Bond Yield data visualizers...")
        subprocess.run([sys.executable, "visualize/vn_bond_yield_visualizer.py"])
        subprocess.run([sys.executable, "visualize/jp_bond_yield_visualizer.py"])
        subprocess.run([sys.executable, "visualize/bond_yield_comparison_visualizer.py"])
        
        print("\nBond Yield data collection and processing completed successfully!")
    else:
        print("\nNo new data found in either crawler. Process stopped.")

if __name__ == "__main__":
    run_bond_yield_crawlers() 