import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

df = pd.DataFrame(columns=["Company","Job Role","Description"])
def getting_data_from_glassdoor():
    #Startup of script
    driver = webdriver.Firefox()
    driver.get("https://www.glassdoor.co.uk/Job/united-kingdom-graduate-software-jobs-SRCH_IL.0,14_IN2_KO15,32.htm")
    #waits and accepts the cookies
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@id='onetrust-accept-btn"
                                                                              "-handler']")))
    cookies = driver.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']")
    cookies.click()

    time.sleep(3)
    finding_links = driver.find_elements(By.XPATH, "//a[@class='JobCard_trackingLink__HMyun']")
    driver.execute_script("arguments[0].scrollIntoView();", finding_links[1])
    finding_links[1].click()

    time.sleep(1)
    close = driver.find_element(By.XPATH, "//button[@class='CloseButton']")
    close.click()

    time.sleep(0)
    # while True:
    finding_links = driver.find_elements(By.XPATH, "//a[@class='JobCard_trackingLink__HMyun']")
    for i in range(len(finding_links)):
        driver.execute_script("arguments[0].scrollIntoView();", finding_links[i])
        ActionChains(driver).move_to_element(finding_links[i]).perform()
        time.sleep(3)
        finding_links[i].click()
        time.sleep(3)
        try:
            # Use WebDriverWait to wait for the company name element to be present
            name_of_company = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h4[@class='heading_Heading__BqX5J heading_Subhead__Ip1aW']"))
            )
            name = name_of_company.get_attribute("outerHTML")
        except Exception as e:
            print(f"Could not find company name for job {i}. Error: {e}")
            name = "N/A"  # Set default value for missing name

        try:
            # Use WebDriverWait to wait for the job role element to be present
            job_role = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h1[@class='heading_Heading__BqX5J heading_Level1__soLZs']"))
            )
            job = job_role.get_attribute("outerHTML")
        except Exception as e:
            print(f"Could not find job role for job {i}. Error: {e}")
            job = "N/A"  # Set default value for missing job role

        main_description = ""
        try:
            # Use WebDriverWait to wait for the job description element to be present
            div_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='JobDetails_jobDescription__uW_fK JobDetails_blurDescription__vN7nh']"))
            )
            main_description = div_element.get_attribute("innerHTML")
        except Exception as e:
            print(f"Could not find job description for job {i}. Error: {e}")
            main_description = "N/A"  # Set default value for missing description

        # Add the scraped data to the DataFrame
        df.loc[i] = [name, job, main_description]
        print(df)
        print(main_description)

        # Save DataFrame to a CSV file
    df.to_csv("Testing.txt", index=False)

# def getting_data_from_gradcracker():
#     driver = webdriver.Firefox()
#     driver.get("https://www.gradcracker.com/search/computing-technology/graduate-jobs")
#     action_for_cookies = driver.find_element(By.XPATH, "//div[@class='tw-px-4 tw-py-2 tw-text-lg tw-font-semibold "
#                                                        "tw-text-gray-100 tw-bg-gray-900 tw-rounded-lg tw-cursor-pointer "
#                                                        "md:tw-px-0 md:tw-py-2 hover:tw-no-underline hover:tw-text-gray-100 "
#                                                        "hover:tw-opacity-80']")
#     action_for_cookies.click()
#     link1 = driver.find_element(By.XPATH, "//div[@class='tw-w-3/5 tw-pr-4 tw-space-y-2']//a")
#     action = ActionChains(driver)
#     action.move_to_element(link1)
#     action.click(link1)
#     action.perform()
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//div[@class='body-content']"))
#         # Update this with an actual unique element from the new page
#     )
#     html = driver.page_source
#     soup = bs.BeautifulSoup(html, 'html.parser')
#     f = open("demo.txt", "a")
#     f.write(soup.prettify())
#     f.close()
#     paragraph = soup.find_all('p')
#     for p in paragraph:
#         print(p.text)
#
#     # allURLs.append(driver.current_url)