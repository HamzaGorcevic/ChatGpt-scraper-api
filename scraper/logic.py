import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def send_message_to_chatgpt(browser, message):
    try:
        # Locate the contenteditable div by its ID
        editable_div = WebDriverWait(browser, 100).until(
            EC.visibility_of_element_located((By.ID, 'prompt-textarea'))
        )
        
        # Scroll the element into view and wait a bit
        browser.execute_script("arguments[0].scrollIntoView(true);", editable_div)
        time.sleep(2)
        
        editable_div.click()
        time.sleep(1)
        editable_div.send_keys(message)

        # Wait for the send button to become enabled and click it
        send_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send prompt' and not(@disabled)]"))
        )
        send_button.click()
        print("Message sent successfully")

        # Wait for the "Stop streaming" button to disappear
        WebDriverWait(browser, 300).until(
            EC.invisibility_of_element_located((By.XPATH, "//button[@aria-label='Stop streaming']"))
        )

        # Wait for the response to be visible
        response_text = get_response(browser)
        return response_text

    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def get_response(browser):
    try:
        response_div = WebDriverWait(browser, 300).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'markdown'))
        )

        response_text = response_div[-1].text if response_div else "No response found."
        return response_text

    except Exception as e:
        print(f"Error retrieving response: {e}")
        return None

def scrape_gpt(msg: str) -> str:
    browser = None
    try:
        options = uc.ChromeOptions()
        
        # Essential options for better stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        
        # Set window size for headless mode
        options.add_argument('--window-size=1920,1080')
        
        # User agent to appear more like a real browser
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Enable headless mode
        options.headless = True
        
        # Initialize the browser with a longer page load timeout
        browser = uc.Chrome(options=options)
        browser.set_page_load_timeout(30)
        
        # Open ChatGPT and wait for initial load
        browser.get("https://chat.openai.com/")
        time.sleep(5)  # Give extra time for the page to fully load
        
        # Send message and get response
        response = send_message_to_chatgpt(browser, msg)
        return response
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        
    finally:
        if browser:
            try:
                browser.quit()
            except Exception as e:
                print(f"Error during browser.quit(): {e}")

