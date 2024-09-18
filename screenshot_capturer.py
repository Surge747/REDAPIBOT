# screenshot_capturer.py

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import time, os

def capture_fullpage_screenshot(url, output_path, driver_path):
    options = Options()
    options.use_chromium = True
    options.add_argument('--headless')
    options.add_argument('--hide-scrollbars')

    # Set a custom user agent
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
    options.add_argument(f'user-agent={user_agent}')

    # Create a Service object
    service = Service(executable_path=driver_path)

    # Use the service parameter instead of executable_path
    driver = webdriver.Edge(service=service, options=options)

    driver.get(url)
    time.sleep(5)  # Wait for the page to load completely

    # Set a fixed width and adjust the window height to capture the full page
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)
    time.sleep(2)  # Wait for the window resize to take effect

    # Create the screenshots folder if it doesn't exist
    screenshots_folder = os.path.dirname(output_path)
    os.makedirs(screenshots_folder, exist_ok=True)

    # Save the screenshot
    driver.save_screenshot(output_path)

    driver.quit()
    return output_path
