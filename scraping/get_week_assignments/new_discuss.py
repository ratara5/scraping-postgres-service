import json, os
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import TimeoutException 

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from getpass import getuser

def get_week_assignments(year, bimester):
    
    options = Options()
    options.add_argument('--profile-directory=Default')
    options.add_argument('--start-maximized')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')  # For container environments option
    options.add_argument('--disable-dev-shm-usage')  # Avoid memory usage issues
    
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36") # Network agent
    
    # WEBDRIVER INITIALIZATION
    service = Service(ChromeDriverManager(driver_version='129.0.6668.58').install())
    driver = webdriver.Chrome(service=service, options=options)
    print('options', options)
    print('service', service)

    # SURF TO WEB
    load_dotenv('../../.env')
    driver.get(os.getenv('URL_PREFIX')+f'/{bimester[0]}-{bimester[1]}-{year}/mwb')
    print('driver: ', driver)
    print('url: ', driver.current_url)
    print('title: ', driver.title)

    # COOKIES
    def accept_cookies(popup):     
        cookies_accept = popup.find_element(By.XPATH, '//html/body/div[1]/div/div/button[1]')
        cookies_accept.click()
    
    print("Sinchronizing with container -> bimester: ", bimester)

    # WEEKS
    container_main = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="toc cms-clearfix"]')))
    weeks = container_main.find_elements(By.XPATH,'//div[@class="syn-body sqs   "]') #weeks in the WorkBook
    print('weeks', weeks)

    weeksprograms_object = {}
    weekprograms_array=[]
    flag_popup = False
    for i in range(1, len(weeks)+1): 
        w={}
        weekdays_a=driver.find_element(By.XPATH, '//*[@id="article"]/div[2]/div[{}]/div[2]/h2/a'.format(i))
        driver.save_screenshot('/app/screenshot.png')
        if flag_popup == False:
            try:
                popup = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '//div[@class="lnc-firstRunPopup"]'))) 
                accept_cookies(popup)
                flag_popup = True
            except TimeoutException:
                print('Accept cookies popup is not present')

        if f"Lectura bíblica para la Conmemoración del {year}" in weekdays_a.text:
           continue

        w["weekdays"] = weekdays_a.text
        w["president"] = "Presidente"

        # Clic in week
        weekdays_a.click()

        # Search reading
        header = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, '//header')))
        reading = header.find_elements(By.XPATH, '//h2/a/strong') #
        reading_text_list = list(map(lambda x: x.text, reading))
        w["reading"] = ' '.join(reading_text_list)
    
        # Search sections
        bodytxt_div = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, '//div[@class="bodyTxt"]')))
        sections = bodytxt_div.find_elements(By.XPATH, '//h2')
        assignments = bodytxt_div.find_elements(By.XPATH, '//h3')

        sections_array=[]
        # sections_array.append({"president":"Presidente"})

        # Section TESOROS
        section_object_1 = {}
        section_object_1["section"] = sections[2].text
        assignments_tesoros_array= []
        i = 1 #assignments[0] is a song
        while i<4:
            assignments_tesoros_array.append(assignments[i].text)
            i+=1
        section_object_1["assignments"] = assignments_tesoros_array
        sections_array.append(section_object_1)


        # Section MAESTROS
        section_object_2 = {}
        section_object_2["section"] = sections[3].text
        assignments_maestros_array = []
        while i<len(assignments):
            if not 'dc-icon--music' in assignments[i].get_attribute('class'): #validate is not song
                assignments_maestros_array.append(assignments[i].text)
                i+=1
            else:
                    i+=1
                    break
        section_object_2["assignments"] = assignments_maestros_array
        sections_array.append(section_object_2)
        
        
        # Section VIDA
        section_object_3 = {}
        section_object_3["section"] = sections[4].text
        assignments_vida_array = []
        while i<len(assignments):
            if not 'dc-icon--music' in assignments[i].get_attribute('class'): #validate is not song
                assignments_vida_array.append(assignments[i].text)
                i+=1
            else:
                i+=1
                break
        new_assignments_vida_array = list(filter(lambda x: x != "", assignments_vida_array))
        new_assignments_vida_array = list(filter(lambda x: not "conclusión" in x, new_assignments_vida_array))
        section_object_3["assignments"] = new_assignments_vida_array 
        sections_array.append(section_object_3)
        # sections_array.append({"final prayer":"Oración final"})


        w["sections"] = sections_array
        w["final_prayer"] = "Oración final"
        weekprograms_array.append(w)
        driver.back() # else end
    weeksprograms_object["bimestral_program"] = weekprograms_array


    pretty_weeksprograms_object = json.dumps(weeksprograms_object, indent=4, ensure_ascii= False)
    print(pretty_weeksprograms_object)
    # print(weeksprograms_object)

    # QUIT WEBDRIVER
    driver.quit()

    return weeksprograms_object # pretty_weeksprograms_object 