import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Website URL
BASE_URL = "https://rera.odisha.gov.in"
PROJECT_LIST_URL = BASE_URL + "/projects/project-list"

# Browser headers to avoid blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Step 1: Get first 6 project detail page links
def get_project_links():
    page = requests.get(PROJECT_LIST_URL, headers=HEADERS)
    soup = BeautifulSoup(page.text, "html.parser")

    project_links = []

    # Find 'View Details' buttons
    buttons = soup.find_all("a", class_="btn-view", href=True)

    for btn in buttons:
        full_link = BASE_URL + btn['href']
        project_links.append(full_link)
        if len(project_links) == 6:
            break

    return project_links

# Step 2: Extract info from project detail page
def get_project_details(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.text, "html.parser")

    # Helper to find table values by label
    def find_text(label):
        label_cell = soup.find("td", string=label)
        if label_cell:
            value_cell = label_cell.find_next_sibling("td")
            return value_cell.text.strip() if value_cell else "N/A"
        return "N/A"

    return {
        "RERA Regd. No": find_text("RERA Registration Number"),
        "Project Name": find_text("Project Name"),
        "Promoter Name": find_text("Company Name"),
        "Promoter Address": find_text("Registered Office Address"),
        "GST No": find_text("GST No."),
        "Detail Page URL": url
    }

# Step 3: Main function
def main():
    print("Getting first 6 project links...")
    links = get_project_links()

    print("Scraping project details...")
    projects = []
    for i, link in enumerate(links, 1):
        print(f"{i}. Scraping: {link}")
        data = get_project_details(link)
        projects.append(data)
        time.sleep(1)  # Be polite to the website

    # Save to CSV
    df = pd.DataFrame(projects)
    df.to_csv("orera_first_6_projects.csv", index=False)
    print("Done! Data saved to 'orera_first_6_projects.csv'")

# Run the main function
if __name__ == "__main__":
    main()
