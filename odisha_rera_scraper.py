from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def scrape_odisha_rera_projects(chromedriver_path: str):
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)

    url = "https://rera.odisha.gov.in/projects/project-list"
    driver.get(url)

    # Wait until projects table loads
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table#tblProjectList tbody tr")))

    projects = driver.find_elements(By.CSS_SELECTOR, "table#tblProjectList tbody tr")[:6]

    data = []

    for project in projects:
        # Click View Details link
        view_details_link = project.find_element(By.LINK_TEXT, "View Details")
        view_details_link.click()

        # Wait for details page to load key field
        wait.until(EC.presence_of_element_located((By.XPATH, "//td[text()='RERA Registration No.']")))

        rera_regd_no = driver.find_element(By.XPATH, "//td[text()='RERA Registration No.']/following-sibling::td").text
        project_name = driver.find_element(By.XPATH, "//td[text()='Project Name']/following-sibling::td").text

        # Click Promoter Details Tab
        promoter_tab = driver.find_element(By.LINK_TEXT, "Promoter Details")
        promoter_tab.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//td[text()='Company Name']")))

        promoter_name = driver.find_element(By.XPATH, "//td[text()='Company Name']/following-sibling::td").text
        address = driver.find_element(By.XPATH, "//td[text()='Registered Office Address']/following-sibling::td").text
        gst_no = driver.find_element(By.XPATH, "//td[text()='GST No.']/following-sibling::td").text

        data.append({
            "RERA Regd. No": rera_regd_no,
            "Project Name": project_name,
            "Promoter Name": promoter_name,
            "Registered Office Address": address,
            "GST No.": gst_no
        })

        driver.back()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table#tblProjectList tbody tr")))

    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv("odisha_rera_projects.csv", index=False)
    print("Scraping completed. Data saved to odisha_rera_projects.csv")

if __name__ == "__main__":
    chromedriver_path = "/path/to/chromedriver"  # <-- CHANGE THIS to your chromedriver path
    scrape_odisha_rera_projects(chromedriver_path)
