import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def retry(func, retries=3, delay=2):
    for attempt in range(retries):
        try:
            func()
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(delay)
    print(f"All {retries} attempts failed.")

def send_message_to_chatgpt(browser,message):
    try:
        # Locate the contenteditable div by its ID
        editable_div = WebDriverWait(browser, 100).until(
            EC.visibility_of_element_located((By.ID, 'prompt-textarea'))
        )
        editable_div.click()
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

        # Wait for the "Send prompt" button to become visible again
        send_button = WebDriverWait(browser, 300).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Send prompt']"))
        )

        # Wait for the response to be visible
        response_text = get_response(browser)
        return response_text

    except Exception as e:
        print(f"Error sending message: {e}")
        print(browser.page_source)

def get_response(browser):
    try:
        response_div = WebDriverWait(browser, 300).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'markdown'))
        )

        response_text = response_div[-1].text if response_div else "No response found."
        print("Response received:", response_text)
        return response_text

    except Exception as e:
        print(f"Error retrieving response: {e}")
        return None



def scrape_gpt(msg:str) ->str:
    browser = None
    try:

        browser = uc.Chrome()

        # Open the ChatGPT page
        browser.get("https://chatgpt.com/")

        response = send_message_to_chatgpt(browser,msg)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if browser is not None:
            try:
                browser.quit()
            except Exception as e:
                print(f"Error during browser.quit(): {e}")

