import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to get the list of categories
def get_categories(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.select('.menu-item-object-wpdmcategory a')
    return [(category['href'], category.text.strip()) for category in categories]

# Function to download a PDF
def download_pdf(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

# Function to scrape PDFs from a category
def scrape_category(url, category_name):
    driver.get(url)
    time.sleep(2)  # Allow time for the page to load

    explore_button = driver.find_element_by_class_name('wpdm-dir-explorer')
    explore_button.click()
    time.sleep(2)  # Allow time for the page to load

    pdf_links = driver.find_elements_by_css_selector('.wpdm-dir-list a.wpdm-download-link')

    pdf_list = []
    for pdf_link in pdf_links:
        pdf_url = pdf_link.get_attribute('data-downloadurl')
        pdf_list.append(pdf_url)

    # Loop through each PDF and download
    for pdf_url in pdf_list:
        download_pdf(pdf_url, f"{category_name}_{pdf_url.split('/')[-1]}")

# Main script
main_url = "https://eprcug.org/"
categories_url = urljoin(main_url, "publications/")
driver = webdriver.Chrome()

try:
    categories = get_categories(categories_url)

    for category_url, category_name in categories:
        scrape_category(category_url, category_name)

finally:
    driver.quit()
