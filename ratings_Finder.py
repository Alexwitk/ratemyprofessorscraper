import time

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Returns to previous webpage if sent to error website
def handle_error_page(page, target_url):
    # Check the current URL
    current_url = page.current_url

    # If the current URL matches the target URL, click the back arrow and refresh so script can progress
    if current_url == target_url:
        page.back()
        page.refresh()
        return True
    # No error page detected
    else:
        return False


# Finds rate my professor data for each professor
def get_professor_rating(driver, professor_name, school):
    # Opens rate my professor website
    driver.get("https://www.ratemyprofessors.com/")
    ratings = []

    # Wait for the close button and close the pop-up if it exists
    try:
        close_button = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div/button")))
        close_button.click()
    except Exception as e:
        print("An error occurred: Closing popup", e)

    # Click the button to switch between searching for schools and professors
    try:
        close_button = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[3]/div[1]/div[4]")))
        close_button.click()
    except Exception as e:
        print("An error occurred: Switching between searching for schools and professors", e)

    # Entering on search to get to next page so can specify University
    try:
        input_element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Search__DebouncedSearchInput-sc-10lefvq-1.fwqnjW")))
        input_element.click()
        input_element.send_keys('Ted')
        input_element.send_keys(Keys.ENTER)
    except Exception as e:
        print("An error occurred: Entering on homepage", e)

    time.sleep(1)
    # Specifying university this way and not on homepage since it wouldn't save otherwise
    try:
        input_element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/div[2]/div/div/div[1]/div/header/div[2]/div[3]/div[1]/div[2]/div/div[2]/div/div/div[2]/input")))

        input_element.click()
        input_element.send_keys("University of Rochester")

    except Exception as e:
        print("An error occurred: Specifying university", e)

    # Find and click on the specific school
    try:
        school_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body/div[2]/div/div/div[1]/div/header/div[2]/div[3]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div/div/ul/li[1]/a")))
        school_option.click()
    except Exception as e:
        print("An error occurred: Selecting university", e)

    # Iterate through all professors
    for prof in professor_name:
        # Check if sent to error page
        handle_error_page(driver, 'https://www.ratemyprofessors.com/error')
        # Enter professor name and search
        try:
            input_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/div[2]/div/div/div[1]/div/header/div[2]/div[3]/div[1]/div[2]/div/div[1]/div[2]/input")))

            input_element.click()
            input_element.send_keys(prof)
            input_element.send_keys(Keys.ENTER)
        except Exception as e:
            print("An error occurred: Entering professor", e)
        # Check if sent to error page
        handle_error_page(driver, 'https://www.ratemyprofessors.com/error')

        # Select first professor in list of professors
        try:
            input_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/div[2]/div/div/div[2]")))
            input_element.click()
        # If not professors found then skip
        except NoSuchElementException:
            print("Hi")
        # Check if sent to error page
        handle_error_page(driver, 'https://www.ratemyprofessors.com/error')
        # Wait for professor cards and find the one matching the school
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'TeacherCard__StyledTeacherCard-syjs0d-0.dLJIlx')))
            professor_cards = driver.find_elements(By.CLASS_NAME, 'TeacherCard__StyledTeacherCard-syjs0d-0.dLJIlx')
            for professor_card in professor_cards:
                try:
                    cur_school = professor_card.find_element(By.CLASS_NAME,
                                                             'CardSchool__School-sc-19lmz2k-1.iDlVGM').text
                    if cur_school == school:
                        professor_card.click()
                        break
                except NoSuchElementException as e:
                    pass
        except TimeoutException as e:
            pass

        # Check if sent to error page
        handle_error_page(driver, 'https://www.ratemyprofessors.com/error')

        # Wait for professor details and fetch the information
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'RatingValue__Numerator-qw8sqy-2.liyUjw')))
            average_score = driver.find_element(By.CLASS_NAME, 'RatingValue__Numerator-qw8sqy-2.liyUjw').text
            average_difficulty = driver.find_element(By.XPATH,
                                                     "//div[contains(text(), 'Level of Difficulty')]/preceding-sibling::div[@class='FeedbackItem__FeedbackNumber-uof32n-1 kkESWs']").text
            take_again_percent = driver.find_element(By.CLASS_NAME,
                                                     'FeedbackItem__FeedbackNumber-uof32n-1.kkESWs').text
            professor_rating = prof + " has an average score of " + average_score + ", an average difficulty of " + average_difficulty + ", and " + take_again_percent + " of students would take their class again"
            ratings.append(professor_rating)
        except TimeoutException as e:
            pass
        except NoSuchElementException as e:
            pass

        # Check if sent to error page
        handle_error_page(driver, 'https://www.ratemyprofessors.com/error')
        # Clicking on button to remove text from field
        try:
            input_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/div[2]/div/div/div[1]/div/header/div[2]/div[3]/div[1]/div[2]/div/div[1]/button")))
            input_element.click()
        except Exception as e:
            print("An error occurred: Clicking x button", e)
    # Write all professor ratings to ratings.txt
    with open('ratings.txt', 'w') as f:
        for rating in ratings:
            f.write(rating + "\n")


# Extension of adblocker
adblocker_extension = r'C:\Users\Alex\Desktop\1.52.2_0'

# Initialize chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('load-extension=' + adblocker_extension)
driver = webdriver.Chrome(options=chrome_options)

# Extract the text content of each line in file
with open('prof.txt', 'r') as file:
    professor_names = [line.strip() for line in file]

# Iterate over the professor names and get their ratings
get_professor_rating(driver, professor_names, "University of Rochester")
# Close the Chrome WebDriver
driver.quit()
