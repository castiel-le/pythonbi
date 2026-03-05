Earnings Call Transcript Downloader
This tool automates the process of mass-downloading earnings call transcripts for multiple companies over a specified year range. It retrieves transcripts as PDFs and converts them into clean text files for data analysis.

Setup Instructions
1. Install Python
Download and install the latest Python 64-bit Windows Installer from the official website:
https://www.python.org/downloads/

Important: During installation, ensure you check the box that says "Add Python to PATH" to use Python from the command line.

2. Upgrade Pip
Open your Command Prompt (cmd) or PowerShell and run the following command to ensure you have the latest version of the package manager:

python -m pip install --upgrade pip

3. Install Dependencies
Navigate to your project folder in the terminal and run the following command to install the required libraries:

pip install -r requirements.txt

Configuration
Before running the script, you must provide an active session cookie to access full transcripts:

1. Log in to discountingcashflows.com in your browser.

2. Press F12 (or Right-Click > Inspect) to open Developer Tools.

3. Navigate to the Application tab (Chrome/Edge) or Storage tab (Firefox).

4. Select Cookies from the left sidebar.

5. Find the sessionid value, copy it, and paste it into the COOKIES dictionary within your Python script.

Execution
To start the download and conversion process, run the following command in your terminal:

python your_filename.py
(Replace your_filename.py with the actual name of your script file.)