# Website_to_scrape : "https://www.topuniversities.com/university-rankings/university-subject-rankings/2022/arts-humanities"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
from selenium.webdriver.chrome.service import Service

columns = ['Rank', 'University', 'Location', 'Overall Score']

def get_uni_details(row):
    details = row.text.split('\n')
    contents = {}
    contents["Rank"] =          details[0]
    contents["University"] =    details[1]
    contents["Location"] =      details[2]
    contents["Country"] =       details[2].strip()
    contents["Overall Score"] = details[-1]
    return contents

def main():
    driver_service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)
    url = f"https://www.topuniversities.com/university-rankings/university-subject-rankings/2022/arts-humanities"
    driver.maximize_window()
    driver.get(url)
    
    uni_data = []

    for _ in range(49):
        rankings = driver.find_element(By.ID, 'ranking-data-load')
        rows = rankings.find_elements(By.XPATH,'//div[contains(@class,"ind") and contains(@class,"row")]')
        for idx, row in enumerate(rows):
            uni_data.append(get_uni_details(row))
        
        button = driver.find_element(By.CSS_SELECTOR, ".page-link.next")
        action = ActionChains(driver)
        action.click(button).perform()
        time.sleep(5)
    
    driver.close()
    
    df = pd.DataFrame(data=uni_data, columns=columns)
    df.to_csv("QS_Art_Hum.csv", index=False)
    return

if __name__ == "__main__":
    main()