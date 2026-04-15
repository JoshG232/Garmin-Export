## Garmin Data Export Tool

This project automates the process of logging into Garmin Connect and downloading activity files (FIT format) for later processing.

### 🚀 Getting Started

#### 1. Prerequisites
You need to have Python installed on your system. This project relies on the `playwright` library for browser automation and `python-dotenv` for managing environment variables.

Install the required Python packages:
```bash
pip install playwright python-dotenv
```

After installing the packages, you must install the necessary browser drivers for Playwright:
```bash
playwright install
```

#### 2. Environment Variables
Create a `.env` file in the root directory (`d:\Code\Python\Garmin Export\`) and add your Garmin credentials:
```env
EMAIL="your_garmin_email@example.com"
PASSWORD="your_garmin_password"
```

#### 3. Running the Script (`bot.py`)
To run the automation script, execute the following command in your terminal:
```bash
python bot.py
```
The script will attempt to log in and then navigate to the activities page to download files.

#### 4. Post-Login Modification (Important!)
**After the initial successful login**, the script will repeatedly attempt to log in. To prevent this, you must comment out the entire login block within `bot.py`.

Look for this section in `bot.py`:
```python
        # Can comment this out after
        if "login" in page.url or await page.query_selector('input[name="email"]') is None:
            print("Not logged in. Attempting login...")
            try:
                await page.wait_for_selector('input[name="email"]', timeout=10000)
                await page.fill('input[name="email"]', USERNAME)
                await page.fill('input[name="password"]', PASSWORD)
                await page.click('button[type="submit"]')
                
                print("Waiting for manual 2FA or login completion...")
                await page.wait_for_url("**/app/home**", timeout=60000)
                print("Login Successful!")
            except Exception as e:
                print(f"Login failed: {e}")
        else:
            print("Already logged in via session cookies!")
```
Comment out the lines from `# Can comment this out after` down to `print(f"Login failed: {e}")` (or just comment out the whole `if` block) to ensure the script runs without attempting to log in every time.

#### 5. Processing Downloads (`FIT/extract.bat`)
The script downloads files into the `FIT/` directory. These files are often compressed into ZIP archives.

To process all downloaded ZIP files and extract their contents, run the batch script:
```bash
.\FIT\extract.bat
```
This script uses WinRAR to extract all `.zip` files found in the `FIT/` directory into the same location and then deletes the original ZIP files.

---
**Note:** Ensure you have WinRAR installed and its path is correctly set in `FIT/extract.bat` if the script fails to run.
`
