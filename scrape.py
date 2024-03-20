import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

if not os.path.exists('data'):
    os.makedirs('data')

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

urls = [
    'https://conversebank.am/en/loans/',
    'https://conversebank.am/en/armenian-resident/',
    'https://conversebank.am/en/young-families/'
]

tags_to_scrape = ['a', 'p', 'h1', 'h2', 'h3']

for index, url in enumerate(urls):
    driver.get(url)
    driver.implicitly_wait(10)

    content = []
    
    for tag_name in tags_to_scrape:
        elements = driver.find_elements(By.TAG_NAME, tag_name)
        for element in elements:
            content_text = element.text.strip()
            if content_text:
                content.append(f"{content_text}\n")
    
    filename = f'data/page{index + 1}.md'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("\n".join(content))

    print(f'Content from {url} saved to {filename}')

driver.quit()
