from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Specify the path to your Firefox profile directory
firefox_profile_path = '/home/my/.mozilla/firefox/gqqy6xzt.default-release'

# Specify the paths for input and output files
input_file_path = '/home/my/Desktop/projects/cdbot/c-input.txt'
output_file_path = '/home/my/Desktop/projects/cdbot/c-output.txt'

# Create FirefoxOptions and set the profile directory
options = webdriver.FirefoxOptions()
options.add_argument(f'--profile={firefox_profile_path}')

# Create the webdriver using the specified profile
driver = webdriver.Firefox(options=options)

# Open a blank tab
driver.execute_script("window.open();")

# Switch to the new tab
driver.switch_to.window(driver.window_handles[1])

# Open the desired URL
url = "https://chat.openai.com/c/37c2b7b5-35d1-45d4-aaa2-41f310261c18"
driver.get(url)

# Wait for Cloudflare protection to load (adjust as needed)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "prompt-textarea")))

# Add additional delays or interactions as needed
# For example, wait for an element to be present before interacting with it
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "prompt-textarea")))

# Initialize a flag to track whether a message has been sent
message_sent = False

def read_and_clear_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    with open(file_path, 'w'):
        pass  # Clear the file
    return content

def filter_and_save_messages(messages, file_path):
    filtered_messages = []
    for i, message in enumerate(messages):
        sender = "User" if i % 2 == 0 else "AI"
        filtered_message = f"{sender}: {message}"
        filtered_messages.append(filtered_message)
    
    with open(file_path, 'w') as output_file:
        output_file.write('\n'.join(filtered_messages))
    
    print(f"Filtered messages and saved to {file_path}")

while True:
    # Check for changes in the c-output.txt file
    try:
        content = read_and_clear_file(output_file_path)
        if content:
            # Send the content as a message to ChatGPT
            message_textarea = driver.find_element(By.ID, "prompt-textarea")
            message_textarea.send_keys(content + Keys.RETURN)
            print(f"Message sent: {content}")
            
            # Set the flag to indicate that a message has been sent
            message_sent = True
    except Exception as e:
        print(f"Error: {e}")

    # Extract text under "data-message-id" only if a message has been sent
    if message_sent:
        try:
            # Add a wait time (adjust as needed)
            time.sleep(5)  # Wait for 5 seconds

            # Wait until the element with aria-label "Stop generating" disappears
            WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Stop generating"]')))
            
            # Add a consistent wait time after "Stop generating" disappears
            time.sleep(6)  # Wait for an additional 6 seconds
            
            messages = driver.find_elements(By.CSS_SELECTOR, '[data-message-id]')
            message_texts = [message.text for message in messages]
            
            # Filter and save the messages with User and AI prefixes
            filter_and_save_messages(message_texts, input_file_path)
        except Exception as e:
            print(f"Error: {e}")

        # Reset the flag after extraction
        message_sent = False

    time.sleep(3)  # Wait for 3 seconds

# Shall the power of AI be on your side :) With that, cdbot is completed, it's basically an unofficial GPT3.5 API, probably illegal, but as a highly developed ape, I use tools to acomplish my goals in the most efficent way.