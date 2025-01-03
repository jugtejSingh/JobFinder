from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import bs4 as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

allURLs = []
def getting_url_from_gradcracker():
    driver = webdriver.Firefox()
    driver.get("https://www.gradcracker.com/search/computing-technology/graduate-jobs")
    action_for_cookies = driver.find_element(By.XPATH, "//div[@class='tw-px-4 tw-py-2 tw-text-lg tw-font-semibold "
                                           "tw-text-gray-100 tw-bg-gray-900 tw-rounded-lg tw-cursor-pointer "
                                           "md:tw-px-0 md:tw-py-2 hover:tw-no-underline hover:tw-text-gray-100 "
                                           "hover:tw-opacity-80']")
    action_for_cookies.click()
    link1 = driver.find_element(By.XPATH, "//div[@class='tw-w-3/5 tw-pr-4 tw-space-y-2']//a")
    action = ActionChains(driver)
    action.move_to_element(link1)
    action.click(link1)
    action.perform()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='body-content']"))
        # Update this with an actual unique element from the new page
    )
    html = driver.page_source
    soup = bs.BeautifulSoup(html, 'html.parser')
    f = open("demo.txt", "a")
    f.write(soup.prettify())
    f.close()
    paragraph = soup.find_all('p')
    for p in paragraph:
        print(p.text)

    # allURLs.append(driver.current_url)


getting_url_from_gradcracker()
