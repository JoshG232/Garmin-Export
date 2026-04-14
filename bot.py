




import asyncio
from playwright.async_api import async_playwright

import os
from dotenv import load_dotenv

load_dotenv()


LOGIN_URL = "https://connect.garmin.com/app/home"
USERNAME = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

async def run():
    async with async_playwright() as p:

        user_data_dir = "./garmin_session"
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )

        page = context.pages[0] # Use the first page that opens automatically
        
        print("Navigating to Garmin...")
        await page.goto("https://connect.garmin.com/app/home")

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

        try:
            await page.goto("https://connect.garmin.com/app/activities")
        except Exception as e:
            print(f"Getting to activities failed: ", {e})

        await page.locator("//*[@id='scrollableArea']/div[1]/div[4]/div[1]/div/div/a").click()
        
        for x in range(0,100):
            await page.locator(".ActivitySettingsMenu_menuContainer__giAbC button").click()
            async with page.expect_download() as download_info:
                await page.get_by_text("Export File", exact=True).click()
            download = await download_info.value
            await download.save_as("./FIT/" + download.suggested_filename)
            await page.get_by_role("button", name="View Previous").click()
            await asyncio.sleep(1)
            
        await asyncio.sleep(20)
        await context.close()

asyncio.run(run())