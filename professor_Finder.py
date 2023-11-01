import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initializes chrome driver
service_obj = Service()
driver = webdriver.Chrome(service=service_obj)
driver.get("https://cdcs.ur.rochester.edu")

# Selects the term field and choose 'Spring 2024'
dropdown_element = driver.find_element(By.NAME, 'ddlTerm')
dropdown = Select(dropdown_element)
dropdown.select_by_visible_text("Spring 2024")

# Finds subject field
dropdown_element = driver.find_element(By.ID, 'ddlDept')
dropdown = Select(dropdown_element)
# Lists all the subject dropdown menu options in list
options = dropdown.options[1:]
subjects = []

for option in options:
    subjects.append(option.get_attribute("value"))

# Set to store all professors found
professor_Set = set()

# Iterate through all subjects
for subject in subjects:
    driver.get("https://cdcs.ur.rochester.edu")
    dropdown_element = driver.find_element(By.NAME, 'ddlTerm')
    dropdown = Select(dropdown_element)
    dropdown.select_by_visible_text("Spring 2024")

    dropdown_element = driver.find_element(By.ID, 'ddlDept')
    # Find the department dropdown element by its name
    dropdown = Select(dropdown_element)
    # Choose specified subject
    dropdown.select_by_value(subject)
    driver.find_element(By.NAME, 'btnSearchTop').click()

    loadingbar_xpath = "/html/body/form/div[3]/table[1]/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr/td[2]/div/div"
    # Waits to give element time to appear
    time.sleep(1)
    # Wait until element disappears to continue
    wait = WebDriverWait(driver, 100)
    element_disappeared = wait.until(EC.invisibility_of_element_located((By.XPATH, loadingbar_xpath)))
    # Find all professors
    instructors_span = driver.find_elements(By.XPATH,
                                            "//span[starts-with(@id, 'rpResults_ctl') and contains(@id, '_lblInstructors')]")

    for instructor in instructors_span:
        professor_name = instructor.text
        # In case multiple professors are teaching the same class
        professor_List = professor_name.split("; ")
        for prof in professor_List:
            if prof in professor_Set:
                continue
            else:
                professor_Set.add(prof)


# Close the WebDriver
driver.quit()

# Write the filtered professors to profList.txt
with open("profList.txt", "w") as file:
    for prof in professor_Set:
        file.write(prof + "\n")
