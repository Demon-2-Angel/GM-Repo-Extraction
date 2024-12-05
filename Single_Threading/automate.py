import subprocess
import time
import os

# Path to the Python file to execute
script_path = r"C:\Users\aniru\Machine Learning\Internships\Virturis Wellness\Task 1 - Scraping\supertums\api.py" # Replace 'script_name.py' with your file name

while True:
    print(f"Starting script execution at {time.ctime()}")
    
    # Start the script using subprocess
    process = subprocess.Popen(["python", script_path])
    
    # Wait for 15 minutes
    time.sleep(900)  # 900 seconds = 15 minutes
    
    # Terminate the process if it's still running
    if process.poll() is None:
        print(f"Stopping script execution at {time.ctime()}")
        process.terminate()
    
    print("Restarting script...")