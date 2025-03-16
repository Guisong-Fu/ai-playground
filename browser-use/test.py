from browser_use import BrowserUse
from playwright.sync_api import sync_playwright
import time

from dotenv import load_dotenv
load_dotenv()

def main():
    # Initialize BrowserUse
    agent = BrowserUse()

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the booking website
        page.goto('https://fp.trafikverket.se/Boka/ng/')

        # Click 'Log in' button
        page.click('text=Logga in')

        # Select BankID authentication
        page.click('text=BankID')

        # Wait for the QR code to appear
        page.wait_for_selector('img[alt="QR code"]')

        # Capture the QR code
        qr_code_element = page.query_selector('img[alt="QR code"]')
        qr_code_src = qr_code_element.get_attribute('src')

        # Display the QR code to the user in your application
        # (Implementation depends on your application's frontend)

        # Wait for user to scan QR code and authenticate
        # (Consider implementing a polling mechanism to check authentication status)

        # Example: Wait for a specific element that indicates successful login
        page.wait_for_selector('text=Welcome', timeout=60000)  # Adjust timeout as needed

        # Function to search for available slots based on user preferences
        def search_and_book_slot():
            # Implement slot search logic here
            # Example: Fill in search criteria and submit the search form
            page.select_option('select#location', 'Preferred Location')
            page.fill('input#date', 'Preferred Date')
            page.click('button#search')

            # Check search results for available slots
            available_slots = page.query_selector_all('div.slot')
            for slot in available_slots:
                # Extract slot details
                slot_time = slot.query_selector('span.time').inner_text()
                slot_location = slot.query_selector('span.location').inner_text()

                # Check if slot matches user preferences
                if slot_time == 'Preferred Time' and slot_location == 'Preferred Location':
                    # Book the slot
                    slot.click()
                    page.click('button#confirm')
                    print(f'Successfully booked slot at {slot_time} in {slot_location}')
                    return True

            return False

        # Continuously search for slots until one is booked
        while True:
            if search_and_book_slot():
                break
            else:
                print('No suitable slots found. Retrying in 10 minutes...')
                time.sleep(600)  # Wait for 10 minutes before retrying

        # Close browser
        browser.close()

if __name__ == '__main__':
    main()